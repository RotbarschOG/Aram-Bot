import requests
"""
This project is based on the API by: https://euw.whatismymmr.com/.
Documentation and licencing can be found on: https://dev.whatismymmr.com/#license.
"""


def get_data(name, region):
    error = None
    if name == "":
        error = 200
        return None, None, None, error
    url = f"https://{region}.whatismymmr.com/api/v1/summoner?name={name}"
    data = requests.get(url).json()
    if "error" in data:
        error = data["error"]["code"]
        return None, None, None, error
    aram_data = data["ARAM"]
    mmr = aram_data["avg"]
    deviation = aram_data["err"]
    rank = aram_data["closestRank"]
    return mmr, deviation, rank, error


def get_mmr(name, region):
    mmr, deviation, rank, err = get_data(name, region)
    # error on the API's part
    if err == 0 or err == 1:
        response = "Unexpected Error."
    # no name was given
    elif err == 200:
        response = "Try using !mmr ign server. The server is EUW by default."
    elif err == 100:
        response = f"Summoner {name} was not found. Check for spelling mistakes or specify your server"
    elif err == 101 or mmr is None or rank is None:
        response = f"Not enough recent games for {name}."
    elif err == 9001:
        response = "Too many requests. Please try again later."
    else:
        response = f"{name} has an ARAM mmr of {mmr} ±{deviation}, which is equal to {rank}."
    return response, rank
