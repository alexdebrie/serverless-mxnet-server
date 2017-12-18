import logging
import os
import shutil

from mms.serving_frontend import ServingFrontend
from mms.model_loader import ModelLoader

logger = logging.getLogger()
logger.setLevel(logging.INFO)

serving_frontend = ServingFrontend(__name__)

model_path = 'squeezenet_v1.1.model'

if os.environ.get('LAMBDA_TASK_ROOT', False):
    shutil.copyfile('/var/task/squeezenet_v1.1.model', '/tmp/squeezenet_v1.1.model')
    model_path = '/tmp/squeezenet_v1.1.model'

models = ModelLoader.load({'squeezenet': model_path})
    
manifest = models[0][3]
service_file = os.path.join(models[0][2], manifest['Model']['Service'])

class_defs = serving_frontend.register_module(service_file)

if len(class_defs) < 1:
    raise Exception('User defined module must derive base ModelService.')
# The overrided class is the last one in class_defs
mode_class_name = class_defs[-1].__name__

# Load models using registered model definitions
registered_models = serving_frontend.get_registered_modelservices()
ModelClassDef = registered_models[mode_class_name]

serving_frontend.load_models(models, ModelClassDef, None)

# Setup endpoint
openapi_endpoints = serving_frontend.setup_openapi_endpoints('127.0.0.1', 8080)

app = serving_frontend.handler.app

if __name__ == "__main__":
    app.run()
