from flask_restful import Resource, reqparse, fields, marshal_with
from flask import jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    jwt_refresh_token_required,
    get_jwt_identity,
    get_raw_jwt
)

import uuid, base62, werkzeug, imageio
from http import HTTPStatus

dnn_fields = {
    'pred_class' : fields.Integer,
    'pred_prob' : fields.Float
}

class DNN(Resource):
    def __init__(self, sess, scaler, dm, dim_x):
        self.sess = sess
        self.scaler = scaler
        self.dm = dm
        self.dim_x = dim_x
        
    @jwt_required
    @marshal_with(dnn_fields)
    def post(self):
        curr_id = get_jwt_identity()

        parse = reqparse.RequestParser()
        parse.add_argument('file', type = werkzeug.datastructures.FileStorage, location='files')
        args = parse.parse_args()

        print("ARGS: {}".format(args))

        image = args['file']
        print("image: {}".format(image))
        
        np_test_xs = imageio.imread(image.stream.read())
        print("{}".format(np_test_xs.shape))        
        np_test_xs = np_test_xs.reshape(-1, self.dim_x).astype(float)
        print("{}".format(np_test_xs.shape))
        #print("{}".format(np_test_xs))
        np_test_xs = self.scaler.transform(np_test_xs)

        with self.sess.graph.as_default():
#             pred_class = model.predict(np_test_xs)
#             print("pred_class: {}".format(pred_class))
        
            pred_class = self.dm.predict_classes(np_test_xs)[0]
            pred_prob = self.dm.predict_proba(np_test_xs)[0]
            print("pred_class: {}".format(pred_class))
            print("pred_prob: {}".format(pred_prob[pred_class]))

            dnn = {}
            dnn['pred_class'] = pred_class
            dnn['pred_prob'] = pred_prob[pred_class]
            return dnn, HTTPStatus.OK
