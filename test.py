from flash_charlotte import *


db = CHARLOTTE_DB('74.80.249.158:5000','augi1234qwer')
print db.add_batch_uniqueKey('dev_table','red',[0])