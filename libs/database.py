from typing import Union, Optional, Any
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.results import InsertOneResult, UpdateResult

from libs.flag import PenaltyPolicyFlag

class Database:
    client = None
    db = None

    def __init__(self, endpoint: str=None) -> None:
        if Database.client == None and endpoint != None:
            Database.client = self.__connect(endpoint=endpoint)
            Database.db = Database.client['bot64']
        self.db = Database.db

    def __connect(self, endpoint: str) -> MongoClient:
        client = MongoClient(host=endpoint)
        client.admin.command('ping') # Raises error if failed
        print('Successfully connected to MongoDB.')
        return client
    
    ''' Private setters and getters '''

    def __get_guild_collection(self) -> Collection:
        return self.db['guild']

    def __insert_guild_document(self, document: dict) -> InsertOneResult:
        return self.__get_guild_collection().insert_one(document=document)

    def __get_guild_document(self, guild_id: str) -> Optional[dict]:
        return self.__get_guild_collection().find_one(filter={ '_id': guild_id })

    def __update_guild_document(self, guild_id: str, update: dict) -> UpdateResult:
        return self.__get_guild_collection().update_one(filter={ '_id': guild_id }, update=update)

    ''' Public setters and getters '''

    def init_guild_config(self, guild_id: str) -> InsertOneResult:
        new_config = {
            '_id': guild_id,
            'log_channel_id': None,
            'timeout_seconds': 60,
            'suspicious_policy': PenaltyPolicyFlag.Ignore.value,
            'malicious_policy': PenaltyPolicyFlag.Timeout.value,
        }
        insertOneResult = self.__insert_guild_document(document=new_config)
        if insertOneResult.inserted_id != guild_id:
            raise Exception('Failed to initialize guild config.')
        return insertOneResult

    def get_guild_config(self, guild_id: str) -> dict:
        config = self.__get_guild_document(guild_id=guild_id)
        if config == None:
            self.init_guild_config(guild_id)
            config = self.__get_guild_document(guild_id=guild_id)
            if config == None:
                raise Exception('Failed to fetch guild config.')

        config['suspicious_policy'] = PenaltyPolicyFlag(config['suspicious_policy']).name
        config['malicious_policy'] = PenaltyPolicyFlag(config['malicious_policy']).name
        return config
    
    def update_guild_config(self, guild_id: str, update: dict) -> UpdateResult:
        self.get_guild_config(guild_id=guild_id) # Make sure guild configuration exists
        return self.__update_guild_document(guild_id=guild_id, update=update)
    
    def set_log_channel_id(self, guild_id: str, log_channel_id: int) -> UpdateResult:
        return self.update_guild_config(guild_id=guild_id, update={ '$set': { 'log_channel_id': log_channel_id } })
    
    def set_timeout_seconds(self, guild_id: str, timeout_seconds: int) -> UpdateResult:
        return self.update_guild_config(guild_id=guild_id, update={ '$set': { 'timeout_seconds': timeout_seconds } })
    
    def set_suspicious_policy(self, guild_id: str, suspicious_policy: PenaltyPolicyFlag) -> UpdateResult:
        return self.update_guild_config(guild_id=guild_id, update={ '$set': { 'suspicious_policy': suspicious_policy.value } })
    
    def set_malicious_policy(self, guild_id: str, malicious_policy: PenaltyPolicyFlag) -> UpdateResult:
        return self.update_guild_config(guild_id=guild_id, update={ '$set': { 'malicious_policy': malicious_policy.value } })
    