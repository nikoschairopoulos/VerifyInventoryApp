import logging
from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver
from .models import Component, DeletedComponent
from pathlib import Path
import json 
from .logging_conf import LOGGING
import logging
import os 
import datetime
from .models import LoggingComponent
from .api.serializers import LogsSerializer
import json

log_dir = 'logs'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

#current directory (is the parent)
CURRENT_DIRECTORY = Path(__file__).parent.absolute()

#Add log files (relative paths)
log_file_component = 'logs/components.logs'

#current file to log
path_file_log = CURRENT_DIRECTORY / log_file_component
print(path_file_log)

################
#set up configs:
################
# Configure logging using the loaded configuration
logging.config.dictConfig(LOGGING)

# Get the new logger
logger = logging.getLogger('component')
#test = 1

#Keep Track of All component
#is a dict of dicts ==> every key is the components PK
_OLD_COMPONENTS_TRACK = {}

@receiver(pre_save,sender=Component)
def store_original_component(sender,instance,**kwargs):
    if instance.pk:
        try:
            existing_instance = Component.objects.get(pk=instance.pk)
            _OLD_COMPONENTS_TRACK[instance.pk] = existing_instance.__dict__.copy()
        except Component.DoesNotExist:
            pass

@receiver(post_save,sender=Component)
def log_component_update(sender, instance, created, **kwargs):
    if created:
        print('a new component has been created')
    else:
        changes = {}
        #this is the updated instance:
        updated_component =  instance.__dict__.copy()
        #iterate over all attributes for the specific PK:
        for attribute,old_value in _OLD_COMPONENTS_TRACK[instance.pk].items():
            if (attribute in updated_component.keys()) and  (old_value != updated_component[attribute]):
                changes.update({attribute:{'old_value':old_value,
                                          'new_value':updated_component[attribute]}
                                })
        try:
            del changes['_state']
            if changes:
                #Add to Log file
                logger.info(f'Component with lci_id: {instance.pk} {datetime.datetime.now()} has been updated with the following changes: {changes}')
            
                log_entry_to_db = LoggingComponent(
                    message = json.dumps(changes),
                    fk = instance                    #here add the entire instance
                )
                #Add to log record to DB:
                log_entry_to_db.save()
        except KeyError:
            pass

@receiver(pre_delete,sender=Component)
def create_copy_of_the_component(sender,instance,**kwargs):
    try:
        deleted_component_to_be_commited_at_db = DeletedComponent(base_component = instance, create_ops = True)
    except Exception as e:
        print(e)
        print(f' {instance.name} deleted component failed to be saved')
        pass


