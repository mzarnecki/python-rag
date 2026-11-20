import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))

from service.document_loader import DocumentLoader  # noqa: E402
from service.document_trimmer import DocumentTrimmer  # noqa: E402
from service.env_loader import load_env  # noqa: E402
from service.services_for_specific_model_factory import ServicesForSpecificModelFactory  # noqa: E402

load_env()
model = os.environ['MODEL']

text_encoder = ServicesForSpecificModelFactory().get_embeddings_service(model)
document_loader = DocumentLoader(text_encoder, DocumentTrimmer())

# load documents
document_loader.load_documents(1330)  # replace this to skip N documents for debugging
