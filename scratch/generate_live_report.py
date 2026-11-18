import sys, os
sys.path.insert(0, os.path.abspath("."))
from app.options.paper_trading.monday_live_session_protocol import MondayLiveSessionProtocol

protocol = MondayLiveSessionProtocol()
report_text = protocol.generate_live_observation_report()
print("Report generated successfully, length:", len(report_text))

