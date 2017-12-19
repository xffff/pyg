import requests, json

class session_manager():
    _ig_url = "https://demo-api.ig.com/gateway/deal/"
    _session_token = ""
    _security_token = ""
    _api_key = ""
    _content_type = "application/json; charset=UTF-8"


    def new_session(self, api_key, identifier, pwd):
        self._api_key = api_key

        URL = self._ig_url + "session"
        data = { "identifier" : identifier, "password" : pwd }
        headers = { "X-IG-API-KEY" : self._api_key \
                    , "Content-Type":  self._content_type \
                    , "Accept" : self._content_type \
                    , "VERSION" : "2"}

        x = requests.post(URL, headers=headers, data=json.dumps(data))
        x.raise_for_status()

        print(x.headers)
        print(json.dumps(x.json(), indent=2))

        self._session_token = x.headers.get("CST")
        self._security_token = x.headers.get("X-SECURITY-TOKEN")
        print("session_token: {}, security_token: {}" \
              .format(self._session_token, self._security_token) )

    def disconnect(self):
        URL = self._ig_url + "session"
        headers = { "X-IG-API-KEY" : self._api_key \
                    , "Content-Type":  self._content_type \
                    , "Accept" : self._content_type \
                    , "X-SECURITY-TOKEN" : self._security_token \
                    , "CST" : self._session_token
        }        

        x = requests.delete(URL, headers=headers)
        x.raise_for_status()

    def list_watchlists(self):
        URL = self._ig_url + "watchlists"
        self.simple_get(URL)

    def get_positions(self):
        URL = self._ig_url + "positions"
        self.simple_get(URL)

    def market_navigation(self):
        URL = self._ig_url + "marketnavigation"
        self.simple_get(URL)

    def get_historical_prices(self \
                              , epic \
                              , resolution \
                              , date_from \
                              , date_to):
        URL = self._ig_url + "prices/" \
              + "{}?resolution={}&from={}&to={}".format(epic \
                                                        , resolution \
                                                        , date_from \
                                                        , date_to)
        self.simple_get(URL)
        
        

    def simple_get(self, url):
        headers = { "X-IG-API-KEY" : self._api_key \
                    , "Content-Type":  self._content_type \
                    , "Accept" : self._content_type \
                    , "X-SECURITY-TOKEN" : self._security_token \
                    , "CST" : self._session_token
        }        

        x = requests.get(url, headers=headers)
        x.raise_for_status()

        print(x.headers)
        print(json.dumps(x.json(), indent=2))




session = session_manager()
session.new_session("USER KEY" \
                    , "USER NAME" \
                    , "PASSWORD")
session.list_watchlists()
session.get_positions()
session.market_navigation()
session.get_historical_prices("MT.D.GC.FWM2.IP", "DAY", "2017-11-21", "2017-11-30")
session.disconnect()
