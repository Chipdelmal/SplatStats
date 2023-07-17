
# https://github.com/cesaregarza/SplatNet3_Scraper

from compress_pickle import dump, load
from splatnet3_scraper.auth import NSO
from splatnet3_scraper.query import QueryHandler 
from splatnet3_scraper.scraper import SplatNet_Scraper

###############################################################################
# Get session token
###############################################################################
# nso = NSO.new_instance()
# print(nso.generate_login_url())

# copied_url = 'REPLACE HERE'
# session_token_code = nso.parse_npf_uri(copied_url)
# session_token = nso.get_session_token(session_token_code)
# dump(session_token, 'session.bz')

###############################################################################
# Test parsing
###############################################################################
session_token = load('./session.bz')
scraper = SplatNet_Scraper(session_token)
summary, battles = scraper.get_vs_battles(mode="turf")

handler = QueryHandler.from_session_token(session_token)
response = handler.query("StageScheduleQuery")
response.data