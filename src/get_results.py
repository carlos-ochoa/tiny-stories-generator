from src.clients import ClientFactory
from src.utils import ConfigManager

cm = ConfigManager('config.yaml')

client = ClientFactory().get_client(
    provider=cm.config['models']['generator_provider'],
    config=cm.config
)

#results = client.get_batch_results("bfd7983f-541a-433f-bae6-aaa77bf389ca")
results = client.check_batch_execution("bfd7983f-541a-433f-bae6-aaa77bf389ca")
print(results)
output_file_stream = client.client.files.download(file_id=results.output_file)
#print(type(output_file_stream.read()))
client.dump_stories(output_file_stream)

print('Outputs written in ', cm.config['data']["output"])