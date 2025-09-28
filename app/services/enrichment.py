import httpx
import logging

from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

log = logging.getLogger(__name__)

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=4),
       retry=retry_if_exception_type(httpx.RequestError))

def fetch_fx_usd_eur() -> float:
    url = "https://api.exchangerate.host/latest?base=USD&symbols=EUR"
    with httpx.Client(timeout=5.0) as client:
        r = client.get(url)
        r.raise_for_status()
        data = r.json()
        rate = data.get("rates", {}).get("EUR")
        log.info("enrichment fx rate fetched")
        return float(rate) if rate is not None else None
    
@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=4),
        retry=retry_if_exception_type(httpx.RequestError))
    
def fetch_fun_fact_short(max_chars: int = 80) -> str:
    url = "https://catfact.ninja/fact"
    with httpx.Client(timeout=5.0) as client:
        r = client.get(url)
        r.raise_for_status()
        data = r.json()
        fact = data.get("fact", "")
        return (fact[:max_chars]).strip()