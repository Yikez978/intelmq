import csv
import StringIO
from intelmq.lib.bot import Bot, sys
from intelmq.lib.event import Event
from intelmq.bots import utils

class ShadowServerQotdParserBot(Bot):

    def process(self):
        report = self.receive_message()

        if report:
            report = report.strip()

            columns = {
                "timestamp": "source_time",
                "ip": "source_ip",
                "protocol" : "transport_protocol",
                "port" : "source_port",
                "hostname": "source_reverse_dns",
                "tag" : "__IGNORE__",
                "quote" : "__IGNORE__",
                "asn": "source_asn",
                "geo": "source_cc",
                "region" : "source_region",
                "city" : "source_city"
            }
            
            rows = csv.DictReader(StringIO.StringIO(report))
            
            for row in rows:
                event = Event()
                
                for key, value in row.items():

                    key = columns[key]

                    if not value:
                        continue

                    value = value.strip()
                    
                    if key is "__IGNORE__" or key is "__TDB__":
                        continue                  
                    
                    event.add(key, value)
            
                event.add('feed', 'shadowserver-qotd')
                event.add('type', 'vulnerable service')
                event.add('protocol', 'qotd')

                event = utils.parse_source_time(event, "source_time")  
                event = utils.generate_observation_time(event, "observation_time")
                event = utils.generate_reported_fields(event)
                
                self.send_message(event)
        self.acknowledge_message()
   

if __name__ == "__main__":
    bot = ShadowServerQotdParserBot(sys.argv[1])
    bot.start()