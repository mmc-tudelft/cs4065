import sys
import os
vse_path = '/home/student/pylib/visual-semantic-embedding/'
if os.path.exists(vse_path):
    sys.path.append(vse_path)
else:
    raise IOError('You need to have "visual-semantic-embedding" git repo\
                  on local path')

import numpy as np
import theano
from theano import tensor as T

import lasagne
from lasagne import layers as L

import demo, tools

class VisualSemanticEmbedder:
    """Joint embedding model for image and text using deep neural nets

    This class is wrapping class for the ryankiros' implementation of
    'visual-semantic-embedding' functionalities.

    It uses Lasagne and Theano for pre-trained networks, so one should
    install them to use this class. Since pre-trained models are deep,
    it requires at least 3 Gib of memory to load the model.

    This wrapper only use MS COCO model for the efficiency purpose.

    This implementation is from "Unifying Visual-Semantic Embeddings with
    Multimodal Neural Language Models" (Kiros, Salakhutdinov, Zemel. 2014).
    """
    def __init__(self,model_path_dict):
        """Initialization requires embedding model path
        """

        self.model_path = model_path_dict

        # compile image feature extractor
        self.vggnet = demo.build_convnet()
        self._get_image_features = theano.function(
            inputs = [self.vggnet['input'].input_var],
            outputs = L.get_output(self.vggnet['fc7'],deterministic=True),
            allow_input_downcast = True
        )

        # load up pretrained VSEM model
        self.model = tools.load_model(
            path_to_model=self.model_path['vse_model']
        )

    def get_image_embedding(self,file_names):
        """
        """
        # check input paths
        if not hasattr(file_names,'__iter__'):
            if isinstance(file_names,str):
                file_names = [file_names]
            else:
                raise ValueError('File names must be a iterable of strings!')

        # (n_images,rgb,width,height)
        X = np.array(map(lambda x:x[0],map(demo.load_image,file_names)))

        # calculate VGG19 image embedding
        Y = self._get_image_features(X).astype(np.float32)

        # project them into VSEM embedding space
        Z = tools.encode_images(self.model,Y)

        return Z

    def get_sentence_embedding(self,sentences):
        """
        """
        # check input paths
        if not hasattr(sentences,'__iter__'):
            if isinstance(sentences,str):
                sentences = [sentences]
            else:
                raise ValueError('Sentences must be a iterable of strings!')

        Z = tools.encode_sentences(self.model,sentences)

        return Z

    def score(self,image_embeddings,sentence_embeddings,method='dot'):
        """
        """
        if method=='dot':
            return np.dot(image_embeddings,sentence_embeddings.T)




