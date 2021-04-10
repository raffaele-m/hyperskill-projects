from calendar_db import Calendar, db, app
from flask import abort
from flask_restful import Api, Resource, reqparse, inputs, fields, marshal_with
from datetime import datetime
import sys

# write your code here
api = Api(app)
event_model = {
    'id': fields.Integer,
    'event': fields.String(80),
    'date': fields.DateTime(dt_format='iso8601'),
}


class TodayEvents(Resource):
    @marshal_with(event_model)
    def get(self):
        today_events = Calendar.query.filter_by(date=datetime.today().strftime('%Y-%m-%d')).all()
        return today_events, 200


class Events(Resource):
    @staticmethod
    def post():
        parser = reqparse.RequestParser()
        parser.add_argument(
            'event',
            type=str,
            help="The event name is required!",
            default=None,
            required=True
        )
        parser.add_argument(
            'date',
            type=inputs.date,
            help="The event date with the correct format is required! The correct format is YYYY-MM-DD!",
            default=None,
            required=True
        )
        args = parser.parse_args()
        event = Calendar(event=args.event, date=args.date)
        db.session.add(event)
        db.session.commit()
        valid_date = datetime.strftime(args.date, '%Y-%m-%d')
        response = {
            "message": "The event has been added!",
            "event": args.event,
            "date": valid_date
        }
        return response, 200

    @marshal_with(event_model)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'start_time',
            type=str,
            help="The start date for the events range with the format YYYY-MM-DD",
            default=None,
            required=False
        )
        parser.add_argument(
            'end_time',
            type=inputs.date,
            help="The end date for the events range with the format YYYY-MM-DD",
            default=None,
            required=False
        )
        args = parser.parse_args()
        if args.start_time is None or args.end_time is None:
            today_events = Calendar.query.all()
            return today_events, 200
        else:
            range_events = Calendar.query.filter((args.start_time <= Calendar.date) & (Calendar.date <= args.end_time)).all()
            return range_events, 200


class EventsByIds(Resource):
    @staticmethod
    @marshal_with(event_model)
    def get(id):
        event = Calendar.query.filter_by(id=id).first()
        if event is None:
            abort(404, "The event doesn't exist!")
        else:
            return event, 200

    @staticmethod
    def delete(id):
        event = Calendar.query.filter_by(id=id).delete()
        if event == 0:
            abort(404, "The event doesn't exist!")
        else:
            db.session.commit()
        response = {
            "message": "The event has been deleted!"
        }
        return response, 200


api.add_resource(TodayEvents, "/event/today")
api.add_resource(Events, "/event")
api.add_resource(EventsByIds, "/event/<int:id>")


if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
