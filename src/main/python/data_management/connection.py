import logging

import pandas as pd
from opensearchpy import OpenSearch, helpers

from data_management import config

'''
  This class is used to connect to the ElasticSearch server.
  It is used to perform the following tasks:
  - Get the index
  - Get the data from the index to a dataframe
  - Insert dataframe into the index
  - Update dataframe from the index
'''
class Connection():

  def __init__(self, host, http_auth, http_compress, use_ssl, verify_certs):
    self.client = self.create_connection(host, http_auth, http_compress, use_ssl, verify_certs)
    self.scrolls  = {}

  def create_connection(self, host, http_auth, http_compress, use_ssl, verify_certs):
    '''
    Create a connection to the Elastic Search index.
    :param host: The host.
    :param http_auth: The authentication user.
    :param http_compress: If compress the index (boolean value).
    :param use_ssl: The SSL.
    :param verify_certs: The certificate.
    '''
    try:
      logging.debug(f'Try open the connection for the host: {host}.')
      return OpenSearch(hosts=host, http_compress=http_compress, http_auth=http_auth, use_ssl=use_ssl, verify_certs=verify_certs)
    except Exception as error:
      logging.error(f'Error opening the connection: {error}')

  def get_index(self, index, query):
    '''
    Retrieve data from Elastic Search server (with limit to 10000 rows and no scroll).
    :param index: The index name stored in Elastic Search.
    :param query: The query to retrieve information.
    '''
    try:
      logging.debug(f'Try recieve data from index: {index} with query: {query}')
      return self.client.search(body=query, index=index,)
    except Exception as error:
      logging.error(f'Error to obtain all index: {error}')

  def read_dataframe(self, index, query=None):
    '''
    Retrieve data in a dataframe from Elastic Search server.
    :param index: The index name stored in Elastic Search.
    :param query: The query to retrieve information.
    :return: A dataframe with the repository extracted from Elastic Search.
    '''
    # print(pd.DataFrame(
    #         map( lambda x : x['_source'], data['hits']['hits'] )
    #           for data in self.create_cursor(index=index, query=query)) .head()
    #     )
    self.scrolls = {}
    return pd.concat([
        pd.DataFrame(
            map( lambda x : x['_source'], data['hits']['hits'] ))
              for data in self.create_cursor(index=index, query=query)
        ])

  def insert_dataframe(self, index, dataframe, key_column=None, delete_index=False):
    '''
    Insert data in the Open Search index from pandas dataframe.
    :param index: The index name in Open Search.
    :param dataframe: The dataframe to insert in the index.
    :param key_column: The column name in dataframe which is key to insert.
    :param delete_index: If delete the existing index before insert new data (optional).
    '''
    if delete_index:
      self.client.indices.delete(index=index, ignore=[400, 404])
    if key_column != None :
      dataframe[key_column] = dataframe[key_column]
    dataframe["_source"] = dataframe.to_dict(orient="records")
    dataframe["_index"] = index
    helpers.bulk(self.client, dataframe[["_source","_index"]].to_dict(orient="records"))

  def update_dataframe(self, index, dataframe, key_column=None, delete_index=False):
    '''
    Update data in the Open Search index from pandas dataframe.
    :param index: The index name in Open Search.
    :param dataframe: The dataframe to update in the index.
    :param key_column: The column name in dataframe which is key to update.
    :param delete_index: If delete the existing index before insert new data (optional).
    '''
    if delete_index:
      self.client.indices.delete(index=index, ignore=[400, 404])
    if isinstance(key_column, list) :
      dataframe["_id"] = pd.util.hash_pandas_object(dataframe[key_column],index=False)
    else:
      dataframe["_id"] = dataframe[key_column]
    dataframe["doc"] = dataframe.loc[:, dataframe.columns!='_id'].to_dict(orient="records")
    dataframe["_op_type"]='update'
    dataframe["_type"]='document'
    dataframe["doc_as_upsert"]=True
    dataframe["_index"] = index
    helpers.bulk(self.client, dataframe[["_op_type","_index","_type","_id","doc","doc_as_upsert"]].to_dict(orient="records"), index=index, doc_type='document')

  def is_open_connection(self):
    """
    Check if the connection to Elastic Search server is open.
    """
    try:
        info = self.client.info()
        logging.debug(f'Connection: {info}')
        return True
    except Exception as error:
        logging.error(f'Error to get connection: {error}')
        return False

  def _get_all_data_start(self, index, query, time):
    '''
    Internal method to get all data from Open Search. Method call from the Cursor class to start to get all data from Open Search.
    :param index: The index name in Open Search.
    :param query: The query to search in the index.
    :param time: The time to scroll.
    '''
    try:
      logging.debug(f'Try recieve data from {index} with {query}')
      response =  self.client.search(body = query, index = index, scroll = time, size = "10000")
      if '_scroll_id' in response:
        self.scrolls[index] = response['_scroll_id']
      return response
    except Exception as error:
      logging.error(f'Error to get all index tasks: {error}')

  def _get_scrolls(self):
    ''' Get scrolls. '''
    return self.scrolls

  def _get_all_data_continue(self, index , time):
    '''
    Internal method to get all data from Open Search. Method call from the Cursor class
    to continue to get all data from Open Search. Note: Error 404 when scroll is not exist.
    :param index: The index name in Open Search.
    :param time: The time to scroll.
    '''
    try:
      scroll_id =  self.scrolls[index]
      time = time
      logging.debug(f'Try recieve data from {scroll_id}')
      return self.client.scroll(scroll_id=scroll_id, scroll=time )
    except Exception as error:
      logging.error(f'Error to get all index tasks: {error}')

  def create_cursor(self, index, query=None, time=None):
    """
    Internal or exteral method to get cursor data from Open Search.
    :param index: The index name in Open Search.
    :param query: The query to search in the index.
    :param time: The time to scroll.
    """
    return self.Cursor(self, index, query, time)


  class Cursor:
      """Class to implement an iterator over cursor opensearch"""

      def __init__(self, connection, index, query, time):
        self.connection = connection
        self.index = index
        self.query = query or config.match_all
        self.time= time or config.scroll_time

      def __iter__(self):
        return self

      def __next__(self):
        if self.index not in self.connection._get_scrolls():
          return self.connection._get_all_data_start(self.index, self.query, self.time)
        result = self.connection._get_all_data_continue(self.index, self.time)
        if result['hits']['hits'] == []:
          raise StopIteration
        return result
