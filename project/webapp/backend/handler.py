from service import ProducerService, SparkService
from youtube import SearchClient
from entity import Video, Channel


class RequestHandler(object):
    # Utility class that handles requests from HTTP server
    search_client = None

    def __init__(self, config):
        if RequestHandler.search_client is None:
            RequestHandler.search_client = SearchClient(key=config["youtube"]["api_key"])

    @staticmethod
    def channel_search(form):
        keyword = form.get("channel_keyword")
        json_data = RequestHandler.search_channel_by_keyword(keyword=keyword, part="snippet")
        return Channel.parse_channel_json(json_data=json_data)

    @staticmethod
    def video_search(form):
        keyword = form.get("video_keyword")
        json_data = RequestHandler.search_client.search_video_by_keyword(keyword=keyword, part='snippet')
        return Video.parse_video_json(json_data=json_data)

    @staticmethod
    def start_spark_streaming(form):
        video_info = form.getlist("video_info")[0].split(":")
        video_id = video_info[0]
        channel_id = video_info[1]
        activity = form["activity"]
        spark_service = SparkService()
        producer_service = ProducerService()
        producer_service.add_argument_pair(producer="file", output_path="/Users/kunliu/Desktop/test")
        producer_service.add_argument_pair(channelId=channel_id, mode="channel_video")
        producer_service.add_argument_pair(videos=video_id+",1,2,3,4,5")
        producer_service.add_argument_pair(activity=activity, write_mode="a",output_mode="d")
        producer_service.start()
        print producer_service.PID

