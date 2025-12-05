"""
🎓 CALL LEARNING SERVICE
========================

Learns from completed calls and improves agent automatically.
Extracts knowledge and rules from conversations.
"""

import logging
import re
from typing import Dict, List

logger = logging.getLogger(__name__)


class CallLearningService:
    """Analyzes calls and improves agents"""
    
    @staticmethod
    def analyze_and_improve(call):
        """
        Main method: Analyze call and update agent
        
        Args:
            call: TwilioCall object
        """
        try:
            if not call or not call.agent:
                logger.warning("⚠️ No call/agent to analyze")
                return False
            
            logger.info(f"🎓 Analyzing call {call.call_sid}")
            
            # Get conversation
            from .models import ConversationLog
            logs = ConversationLog.objects.filter(call=call).order_by('id')
            
            if not logs.exists():
                logger.warning("⚠️ No conversation logs found")
                return False
            
            # Extract learnings
            knowledge = []
            rules = []
            
            for i in range(len(logs) - 1):
                current = logs[i]
                next_msg = logs[i + 1] if i + 1 < len(logs) else None
                
                # KNOWLEDGE: Customer asks → Agent answers
                if current.role == 'user' and CallLearningService._is_question(current.message):
                    if next_msg and next_msg.role == 'assistant':
                        category = CallLearningService._categorize(current.message)
                        knowledge.append({
                            'category': category,
                            'q': current.message,
                            'a': next_msg.message
                        })
                        logger.info(f"📚 Knowledge: {category}")
            
            # RULES: Successful patterns (if call converted)
            if call.status == 'completed' and call.duration > 60:
                for log in logs:
                    if log.role == 'user' and CallLearningService._is_objection(log.message):
                        # Find agent response
                        idx = list(logs).index(log)
                        if idx + 1 < len(logs):
                            response = logs[idx + 1]
                            if response.role == 'assistant':
                                rules.append({
                                    'type': 'objection',
                                    'trigger': log.message,
                                    'response': response.message
                                })
                                logger.info(f"✅ Rule: Objection handling")
            
            # Update agent
            if knowledge:
                CallLearningService._update_knowledge(call.agent, knowledge)
            
            if rules:
                CallLearningService._update_rules(call.agent, rules)
            
            logger.info(f"✅ Agent improved: {len(knowledge)} knowledge + {len(rules)} rules")
            return True
            
        except Exception as e:
            logger.error(f"❌ Learning error: {e}")
            return False
    
    @staticmethod
    def _is_question(text: str) -> bool:
        """Check if text is a question"""
        indicators = ['?', 'what', 'how', 'why', 'when', 'can you', 'do you']
        return any(ind in text.lower() for ind in indicators)
    
    @staticmethod
    def _is_objection(text: str) -> bool:
        """Check if text is an objection"""
        objections = ['expensive', 'too much', 'not interested', 'not sure', 'think about']
        return any(obj in text.lower() for obj in objections)
    
    @staticmethod
    def _categorize(question: str) -> str:
        """Categorize question"""
        q = question.lower()
        if any(w in q for w in ['price', 'cost', 'pay']):
            return 'pricing'
        elif any(w in q for w in ['feature', 'does it', 'can it']):
            return 'features'
        elif any(w in q for w in ['company', 'who are you']):
            return 'company_info'
        else:
            return 'general'
    
    @staticmethod
    def _update_knowledge(agent, knowledge_list: List[Dict]):
        """
        Update agent knowledge_files (merges with existing structure)
        
        Agent.knowledge_files structure (JSONField):
        {
            'pricing': 'Q: How much? A: $99/month',
            'features': 'Q: What features? A: AI calling...',
            'company_info': 'Q: Who are you? A: We are...',
            'general': 'Other Q&A pairs'
        }
        """
        try:
            from agents.models import Agent
            
            # Get current knowledge (preserve existing data)
            current = agent.knowledge_files or {}
            
            for item in knowledge_list:
                cat = item['category']  # pricing, features, company_info, general
                qa = f"Q: {item['q']}\nA: {item['a']}"
                
                # Check duplicate (don't add same Q&A twice)
                if cat in current and qa in str(current[cat]):
                    logger.debug(f"⏭️ Skip duplicate: {cat}")
                    continue
                
                # Add new knowledge (append to existing category)
                if cat in current:
                    current[cat] += f"\n\n{qa}"
                else:
                    current[cat] = qa
                
                logger.info(f"📚 Added to knowledge_files['{cat}']")
            
            # Save updated knowledge_files
            agent.knowledge_files = current
            agent.save(update_fields=['knowledge_files'])
            
            # 🔥 SYNC TO HUMEAI: Update HumeAI config with new knowledge
            CallLearningService._sync_to_humeai(agent)
            
        except Exception as e:
            logger.error(f"❌ Knowledge update error: {e}")
    
    @staticmethod
    def _update_rules(agent, rules_list: List[Dict]):
        """
        Update agent sales_script_text (appends learned patterns)
        
        Agent.sales_script_text structure (TextField):
        - Contains full 3-step sales script
        - May come from manual input OR website_url scraping
        - We APPEND learned objection handling patterns
        """
        try:
            from agents.models import Agent
            
            # Get current script (preserve existing structure)
            current_script = agent.sales_script_text or ""
            
            # Learned rules section header
            learned_section = "\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            learned_section += "\n🎓 LEARNED OBJECTION HANDLING (From Real Calls):"
            learned_section += "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            
            # Check if learned section already exists
            if "🎓 LEARNED OBJECTION HANDLING" not in current_script:
                current_script += learned_section
            
            for rule in rules_list:
                if rule['type'] == 'objection':
                    rule_text = f"\n\n🎯 When customer says: '{rule['trigger'][:50]}...'"
                    rule_text += f"\n   Respond: '{rule['response'][:100]}...'"
                    
                    # Check duplicate (60% keyword similarity)
                    trigger_words = set(re.findall(r'\w+', rule['trigger'].lower()))
                    trigger_words = {w for w in trigger_words if len(w) > 3}
                    
                    if trigger_words:
                        matches = sum(1 for w in trigger_words if w in current_script.lower())
                        similarity = matches / len(trigger_words)
                        
                        if similarity > 0.6:
                            logger.debug(f"⏭️ Skip duplicate rule (similarity: {similarity:.0%})")
                            continue
                    
                    # Append learned rule
                    current_script += rule_text
                    logger.info(f"✅ Added learned rule to sales_script_text")
            
            # Save updated script
            agent.sales_script_text = current_script
            agent.save(update_fields=['sales_script_text'])
            
            # 🔥 SYNC TO HUMEAI: Update HumeAI config with new rules
            CallLearningService._sync_to_humeai(agent)
            
        except Exception as e:
            logger.error(f"❌ Rules update error: {e}")
    
    @staticmethod
    def _sync_to_humeai(agent):
        """Update HumeAI config prompt when agent learns"""
        try:
            # Only sync outbound agents with HumeAI config
            if agent.agent_type != 'outbound' or not agent.hume_config_id:
                logger.debug(f"⏭️ Skip HumeAI sync: Not outbound or no config")
                return
            
            from HumeAiTwilio.hume_agent_service import hume_agent_service
            
            logger.info(f"🔄 Updating HumeAI config prompt: {agent.hume_config_id}")
            
            # Build updated system prompt with new knowledge/rules
            updated_prompt = hume_agent_service._build_system_prompt(
                base_prompt=f"You are {agent.name}, an AI assistant.",
                agent_obj=agent  # This has updated knowledge_files and sales_script_text
            )
            
            # Update existing config (no delete/recreate)
            success = hume_agent_service.update_agent(
                config_id=agent.hume_config_id,
                system_prompt=updated_prompt
            )
            
            if success:
                logger.info(f"✅ HumeAI config prompt updated with learned knowledge/rules")
            else:
                # Fallback: If PATCH doesn't work, create new config
                logger.warning(f"⚠️ PATCH failed, creating new config version")
                
                new_config_id = hume_agent_service.create_agent(
                    name=agent.name,
                    system_prompt=f"You are {agent.name}, an AI assistant.",
                    voice_name='Ito',
                    language='en',
                    agent_obj=agent
                )
                
                if new_config_id:
                    # Delete old config
                    hume_agent_service.delete_agent(agent.hume_config_id)
                    
                    # Update with new config ID
                    agent.hume_config_id = new_config_id
                    agent.save(update_fields=['hume_config_id'])
                    logger.info(f"✅ HumeAI config recreated: {agent.hume_config_id} → {new_config_id}")
                else:
                    logger.error(f"❌ Both PATCH and recreate failed")
                
        except Exception as e:
            logger.error(f"❌ HumeAI sync error: {e}")


# Global instance
call_learning_service = CallLearningService()
