import webapp2
from google.appengine.ext import db

from proto import sample_pb2
from goog.protobuf import text_format


class Data(db.Model):
    proto = db.BlobProperty()


class WritePage(webapp2.RequestHandler):
    def get(self):
        sample = sample_pb2.MyData()
        sample.name = 'My Name'
        sample.age = 18
        child = sample.child.add()
        child.name = 'Child!'
        child.age = 50
        child = sample.child.add()
        child.name = 'Child2!'
        child.age = -1

        serialized = sample.SerializeToString()
        data = Data(proto=serialized)
        data.put()

        stored_data = list(Data.gql(''))[0]
        stored_sample = sample_pb2.MyData()
        # We don't need to convert google.appengine.api.datastore_types.Blob
        # to str before ParseFromString.
        stored_sample.ParseFromString(stored_data.proto)
        stored_data.delete()

        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Serialized: ' + `serialized` + '\n')
        self.response.write(''.join(['type(stored_data.proto): ',
                                     str(type(stored_data.proto)), '\n']))
        self.response.write(text_format.MessageToString(stored_sample))


application = webapp2.WSGIApplication([
        ('/', WritePage),
        ], debug=True)
