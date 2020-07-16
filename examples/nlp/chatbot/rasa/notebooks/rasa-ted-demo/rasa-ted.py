#!/usr/bin/env python
# coding: utf-8

# # Rasa TED Demo



import os
import asyncio

from rasa.nlu.training_data import load_data 
from rasa.nlu.model import Trainer
from rasa.nlu import config
from rasa.nlu.model import Interpreter


# In[2]:


#get_ipython().system('ls ../../rasa-ted-demo')


# In[5]:


root_dir = '../../rasa-ted-demo'


# In[7]:


data_path = os.path.abspath(os.path.join(root_dir, 'data/nlu.md'))
config_path = os.path.abspath(os.path.join(root_dir, 'config.yml'))
model_dir = os.path.abspath(os.path.join(root_dir, 'models'))


# ----------------

# In[10]:


training_data = load_data(data_path)


# In[11]:


trainer = Trainer(config.load(config_path))


# In[12]:


trainer.train(training_data)


# In[13]:


model_directory = trainer.persist(model_dir, fixed_model_name="current")


# ----------------

# In[14]:


interpreter = Interpreter.load(os.path.join(model_dir, 'current'))


# In[15]:


text = 'count'
interpreter.parse(text)


# ------------------

# In[16]:


import asyncio


# In[17]:


from rasa.core import config
from rasa.core.agent import Agent


# In[21]:


#get_ipython().system('ls ../../rasa-ted-demo/*')


# In[18]:


root_dir = '../../rasa-ted-demo'


# In[22]:


domain_config = os.path.abspath(os.path.join(root_dir, 'domain.yml'))
policy_config = os.path.abspath(os.path.join(root_dir, 'config.yml'))
training_data_file = os.path.abspath(os.path.join(root_dir, 'data/stories.md'))
model_dir = os.path.abspath(os.path.join(root_dir, 'models'))
policy_fixed_model_name="dialogue"


# ------------

# In[23]:


policies = config.load(policy_config)


# In[24]:


agent = Agent(domain_config,
              policies=policies)


# In[25]:
loop = asyncio.get_event_loop()
training_data = loop.run_until_complete(agent.load_data(training_data_file))


# In[26]:


agent.train(training_data)


# In[27]:


agent_model_path = os.path.join(model_dir, policy_fixed_model_name)


# In[28]:


agent.persist(agent_model_path)


# In[29]:


#get_ipython().system('ls ../../rasa-ted-demo/*')


# In[36]:


#get_ipython().system('ls ../../rasa-ted-demo/models/dialogue/core')


# ---------------------

# In[37]:


from rasa.core.agent import Agent
from rasa.core.interpreter import NaturalLanguageInterpreter
from rasa.core.utils import EndpointConfig


# In[38]:


model_directory = os.path.join(model_dir, "current")


# In[39]:


interpreter = NaturalLanguageInterpreter.create(model_directory)


# In[40]:


action_endpoint = EndpointConfig(url="http://localhost:5055/webhook")


# In[41]:


agent_model_path = os.path.join(model_dir, policy_fixed_model_name)
agent = Agent.load(agent_model_path, 
                   interpreter=interpreter,
                   action_endpoint=action_endpoint)


# In[44]:

loop = asyncio.get_event_loop()
rst = loop.run_until_complete(agent.parse_message_using_nlu_interpreter("count"))


# In[45]:


print(rst)


# In[46]:
umsg="hi"
print(umsg)
loop = asyncio.get_event_loop()
responses = loop.run_until_complete(agent.handle_text(text_message=umsg, sender_id='1'))


# In[47]:


print(responses)


# In[48]:
umsg="count"
print(umsg)
loop = asyncio.get_event_loop()
responses = loop.run_until_complete(agent.handle_text(text_message=umsg, sender_id='1'))
print(responses)


# In[49]:

umsg="ok"
print(umsg)
loop = asyncio.get_event_loop()
responses = loop.run_until_complete(agent.handle_text(text_message=umsg, sender_id='1'))
print(responses)


# In[50]:

umsg="are you a bot?"
print(umsg)
loop = asyncio.get_event_loop()
responses = loop.run_until_complete(agent.handle_text(text_message=umsg, sender_id='1'))
print(responses)


# In[51]:

umsg="ok"
print(umsg)
loop = asyncio.get_event_loop()
responses = loop.run_until_complete(agent.handle_text(text_message=umsg, sender_id='1'))
print(responses)


# In[52]:

umsg="hi"
print(umsg)
loop = asyncio.get_event_loop()
responses = loop.run_until_complete(agent.handle_text(text_message=umsg, sender_id='1'))
print(responses)


# In[53]:

umsg="ok"
print(umsg)
loop = asyncio.get_event_loop()
responses = loop.run_until_complete(agent.handle_text(text_message=umsg, sender_id='1'))
print(responses)


# In[ ]:




