import uuid
from cassandra.cqlengine import columns
from cassandra.cqlengine.usertype import UserType
from cassandra.cqlengine.models import Model


class User(Model):
    user_id = columns.UUID(primary_key=True, default=uuid.uuid4)
    reputation = columns.Integer(primary_key=True, default=0)
    first_name = columns.Text(required=True, max_length=50)
    last_name = columns.Text(required=True, max_length=50)


class UserLogin(Model):
    email = columns.Text(required=True, max_length=100, primary_key=True)
    username = columns.Text(required=True, max_length=50, index=True)
    password = columns.Text(required=True, min_length=6, max_length=50)
    user_id = columns.UUID()


class Picture(Model):
    pic_uuid = columns.UUID(primary_key=True, default=uuid.uuid4)
    data = columns.Blob()
    user_id = columns.UUID()


# This is a user defined type
class Link(UserType):
    link_id = columns.UUID(primary_key=True)
    url = columns.Text()
    comment = columns.Text(max_length=200)
    time_tag = columns.Text(min_length=2, max_length=10)


class Video(Model):
    video_id = columns.UUID(primary_key=True, default=uuid.uuid4)
    language = columns.Text(min_length=1, max_length=100, default='English', partition_key=True)
    correctness = columns.Decimal(default=0.0, primary_key=True)
    video_codec = columns.Text()
    user_id = columns.UUID()
    date_created = columns.DateTime(index=True)
    title = columns.Text(required=True, max_length=500)
    description = columns.Text(min_length=1, max_length=1000)
    data = columns.Text(required=True)
    links = columns.List(value_type=columns.UserDefinedType(Link))


class Vote(Model):
    vote = columns.Set(value_type=columns.Integer)
    video_id = columns.UUID(primary_key=True)


class Playlist(Model):
    playlist_id = columns.UUID(primary_key=True, default=uuid.uuid4)
    playlist_name = columns.Text(min_length=1, max_length=200)
    vid_order = columns.Integer(required=True, primary_key=True)
    video_id = columns.UUID()
    user_id = columns.UUID(primary_key=True)


class Viewing(Model):
    video_id = columns.UUID(primary_key=True)
    user_id = columns.UUID(primary_key=True)
    stopped_at = columns.Text(min_length=2, max_length=10)

