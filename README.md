# SW-Engineer-Tech-Challenge
Hello and welcome to our software challenge, we're glad to have you here 👋

Right away, **a note on how to work on and submit the challenge**: Please fork this repository using the Fork button in the upper right on the repository start site.
You can work on the challenge in your fork then (more detailed information is provided in the challenge description linked above).
**For submission, please do not create a pull request.**

This repository contains template code and sample data that you can use during the challenge.
The description of the challenge, which contains all information you should need to solve the challenge, can be found here: [Challenge description](https://floyai.atlassian.net/wiki/external/84377616/NmZjYjZkZmJkYTcxNGNlMDgyODQ0OWUzYWYxNjZhY2I?atlOrigin=eyJpIjoiNTg3N2E0NTVhMjBlNDVmM2I1NGNiNmVmOWMwZGRiZmEiLCJwIjoiYyJ9).

We recommend you to read this document carefully.
If we update this document during the challenge, we will inform you about this separately.


We wish you a lot of fun and success with the challenge 🚀

# Regarding my solution

## Notes
- The data is automatically processed when sent by the PACS.
- It is then stored in a file based sqlite database on server side (series_data.db) 

### Running
- install python dependencies `pip install -r requirements.txt`
- start server with `uvicorn server:app`
- start client with `python client.py`
- start sending data over PACS

## Planning Documents
General description from the processing pipeline of a set of datasets:

![sequence diagram](https://www.plantuml.com/plantuml/png/TP6nJiCm48PtFyMDC32mPa0jYSI4LCW3LCO-g2N7PzddLBmzbpP44AVh_zt_wxEyowmJby4hRPWI7FPjhw94phYe0yChMUqTV_T2iMyF_s2FoM7kN8wQpGdJ1cp9UvJfYesOG2bF5A44TXu2GS0pMCqw8yEds3n2HaF1gaaB7fug6sXaAbZehYLLSUci9QMpjqi5cE2jO45LtKbtzOO6KWd7V0cFvZVDTxFplK9nNNLkABmWGqj3zCYuwDzG637zVQWepwcQePnDu4D6v4wFE9rqpmlUD7Z774acpuvFqBFcahS5Lba37Lwi3QLqtN3Xg_hkdUYMmVy0)

Class diagram:

![class diagram](https://www.plantuml.com/plantuml/png/TL9DRnmX3BtpApXk3kaF6FMGA6cbbVgnrRIdga8EE0ag0rCmKLTf_dlDm6IwQBjxOFpmUxOVlae4aVBan0pw9poWrCwY9_aij8EKv8ZHOhe9pg6c41bF2wAiPwhNgB8rWqmKsyNGA8BffF9iW52HdN2Gzou02MFJ3AGVrL8QcNmNWXEA5IqfjMC29AGB0SQyLjdGbvF6RfiOncVXGfW7UPsENjlmvWD7ubV6Z1lsfOHY2WQSfQDAclC_jcZawN2yEQppwNNaeVVW-u-jsGinWVLynEnLpqoCRzDsbto7loc29bLc-pULGib-mfBpml_rQIguFSqQminpl8T4ruUzA8sPEsOUFezV1yacjjAxUdIIUdxLwvqeoiMyTs8nYf5QiHaDPuo64wDvM7zl7t941SWTFO8t3bKg-ZjyGa-dpV33e4lTwd5OF_Pj5RxjR-k-IVuTWCgwVe89Uv1AdlMqG2DbSpohi8AiN-jKKkchDV3sp-LblmEYDwjczKifEjf_igxGcpovlm00)

## Time taken
- 30 Minutes Research on DICOM and testing out PACS
- 20 minute planning
- 1 hour implementing functions
- 1 hour implementing tests
- 15 minutes refining planning diagrams