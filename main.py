import requests
import json
import os


def main(args={}):
    config = {
        "api": "https://api.lolicon.app/setu/v2",
        # "api": "https://net.lolicon.app/ua",
        "r18": True,
        "num": 10,

        "path": "./download/",

        "timeout": 30,
        "excludeAI": True,
        "proxy": "i.pixiv.re",
    }

    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                      " AppleWebKit/537.36 (KHTML, like Gecko)"
                      " Chrome/108.0.0.0"
                      " Safari/537.36"
                      " Edg/108.0.1462.46",
        "Content-Type": "application/json"
    }

    payload = {
        "r18": config["r18"],
        "num": config["num"],
        "excludeAI": config["excludeAI"],
        "proxy": config["proxy"]
    }

    if args["number"]:
        for i in range(int(args["number"] / config["num"])):
            temp = getApiResponse(config, payload, header)

            isError = temp[0]
            response = temp[1]

            if not isError:
                resJson = json.loads(response.text)
                downloadImage(resJson, config, header)

    return 0


def getApiResponse(config, payload, header):
    isError = True

    try:
        response = requests.post(config["api"],
                                 headers=header,
                                 data=json.dumps(payload),
                                 timeout=config["timeout"]
                                 )
        if response.status_code == 200:
            isError = False
    except requests.exceptions.ConnectTimeout:
        return [isError, "timeout"]

    return [isError, response]


def downloadImage(resJson, config, header):
    for res in resJson["data"]:
        fileName = "[" + res["title"].replace("/", "-") + "]" + \
                   "_pid-" + str(res["pid"]) + \
                   "_author-" + res["author"].replace("/", "-") + \
                   "." + res["ext"]
        filePath = config["path"] + fileName

        if not os.path.exists(filePath):
            print("downloading: " + (res["title"] + "-" + res["urls"]["original"]))
            try:
                with open(filePath, "wb") as file:
                    try:
                        file.write(
                            requests.get(
                                res["urls"]["original"],
                                headers=header,
                                timeout=config["timeout"]
                            ).content
                        )
                    except requests.exceptions.ConnectTimeout:
                        print("download failed(timeOut): " + (res["title"] + "-" + res["urls"]["original"]))
                        if os.path.exists(filePath):
                            os.remove(filePath)
            except OSError:
                print("download failed(fileError): " + (res["title"] + "-" + res["urls"]["original"]))
                if os.path.exists(filePath):
                    os.remove(filePath)
        print("download success: " + (res["title"] + "-" + res["urls"]["original"]))


if __name__ == '__main__':
    main({
        "number": 100
    })
