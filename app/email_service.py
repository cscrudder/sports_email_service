import os
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


load_dotenv()

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
SENDER_EMAIL_ADDRESS = os.getenv("SENDER_EMAIL_ADDRESS")
RECIPIENT_EMAIL_ADDRESS = os.getenv("RECIPIENT_EMAIL_ADDRESS")

def send_email(subject="Daily Hockey Report", html="<p>Hello World</p>", recipient_address=RECIPIENT_EMAIL_ADDRESS):
    """
    Sends an email with the specified subject and html contents to the specified recipient,

    If recipient is not specified, sends to the admin's sender address by default.
    """
    client = SendGridAPIClient(SENDGRID_API_KEY) #> <class 'sendgrid.sendgrid.SendGridAPIClient>
    print("CLIENT:", type(client))
    print("SUBJECT:", subject)
    #print("HTML:", html)

    message = Mail(from_email=SENDER_EMAIL_ADDRESS, to_emails=recipient_address, subject=subject, html_content=html)
    try:
        response = client.send(message)
        print("RESPONSE:", type(response)) #> <class 'python_http_client.client.Response'>
        print(response.status_code) #> 202 indicates SUCCESS
        return response
    except Exception as e:
        print("OOPS", type(e), e)
        return None


if __name__ == "__main__":

    from datetime import date
    today = date.today().strftime("%b %d %Y")

    example_subject = "NHL Daily Briefing: " + today

    example_html = f"""
<p>Hey Jack,</p><p>Here is your daily update!</b><h1>Today's Recommended Game:</h1><ul><li><b>Dallas Stars at Edmonton Oilers</b> (8:30PM ET)<ul style="list-style-type: circle; padding-bottom: 0;"><li style="margin-left:em">Records: Stars (43W-28L) | Oilers (44W-26L)</li><li style="margin-left:em">Broadcasts: NHL Network (national), SN360 (international), SNW (international), TVAS (international) and BSSWX (away)</li></ul></li></ul><h1>Today's Schedule:</h1><ul><li><b>Dallas Stars at Edmonton Oilers</b> (8:30PM ET)<ul style="list-style-type: circle; padding-bottom: 0;"><li style="margin-left:em">Records: Stars (43W-28L) | Oilers (44W-26L)</li><li style="margin-left:em">Broadcasts: NHL Network (national), SN360 (international), SNW (international), TVAS (international) and BSSWX (away)</li></ul></li><li><b>Washington Capitals at Vegas Golden Knights</b> (10PM ET)<ul style="list-style-type: circle; padding-bottom: 0;"><li style="margin-left:em">Records: Capitals (43W-23L) | Golden Knights (41W-31L)</li><li style="margin-left:em">Broadcasts: SportsNet RM (home) and NBCS-DC (away)</li></ul></li><li><b>Colorado Avalanche at Seattle Kraken</b> (10PM ET)<ul style="list-style-type: circle; padding-bottom: 0;"><li style="margin-left:em">Records: Avalanche (55W-15L) | Kraken (25W-44L)</li><li style="margin-left:em">Broadcasts: ROOT Sports NW (home) and ALT (away)</li></ul></li><li><b>Chicago Blackhawks at Arizona Coyotes</b> (10PM ET)<ul style="list-style-type: circle; padding-bottom: 0;"><li style="margin-left:em">Records: Blackhawks (25W-40L) | Coyotes (22W-49L)</li><li style="margin-left:em">Broadcasts: BSAZX (home) and NBCS-CHI 
(away)</li></ul></li></ul><h1>League Standings:</h1><h3>Pacific Division Standings</h3><table><tr><th>Rank</th><th>Team</th><th>Wins</th><th>Losses</th><th>Ties</th><th>Points</th></tr><tr><td>1</td><td>Calgary Flames</td><td>47</td><td>20</td><td>10</td><td>104</td></tr><tr><td>2</td><td>Edmonton Oilers</td><td>44</td><td>26</td><td>6</td><td>94</td></tr><tr><td>3</td><td>Los Angeles Kings</td><td>41</td><td>27</td><td>10</td><td>92</td></tr><tr><td>4</td><td>Vegas Golden Knights</td><td>41</td><td>31</td><td>5</td><td>87</td></tr><tr><td>5</td><td>Vancouver Canucks</td><td>38</td><td>28</td><td>11</td><td>87</td></tr><tr><td>6</td><td>Anaheim Ducks</td><td>30</td><td>34</td><td>14</td><td>74</td></tr><tr><td>7</td><td>San Jose Sharks</td><td>30</td><td>34</td><td>12</td><td>72</td></tr><tr><td>8</td><td>Seattle 
Kraken</td><td>25</td><td>44</td><td>6</td><td>56</td></tr></table><h3>Central Division Standings</h3><table><tr><th>Rank</th><th>Team</th><th>Wins</th><th>Losses</th><th>Ties</th><th>Points</th></tr><tr><td>1</td><td>Colorado Avalanche</td><td>55</td><td>15</td><td>6</td><td>116</td></tr><tr><td>2</td><td>Minnesota Wild</td><td>48</td><td>21</td><td>7</td><td>103</td></tr><tr><td>3</td><td>St. Louis Blues</td><td>46</td><td>20</td><td>11</td><td>103</td></tr><tr><td>4</td><td>Nashville Predators</td><td>44</td><td>28</td><td>5</td><td>93</td></tr><tr><td>5</td><td>Dallas Stars</td><td>43</td><td>28</td><td>5</td><td>91</td></tr><tr><td>6</td><td>Winnipeg Jets</td><td>35</td><td>31</td><td>11</td><td>81</td></tr><tr><td>7</td><td>Chicago Blackhawks</td><td>25</td><td>40</td><td>11</td><td>61</td></tr><tr><td>8</td><td>Arizona Coyotes</td><td>22</td><td>49</td><td>5</td><td>49</td></tr></table><h3>Metropolitan Division Standings</h3><table><tr><th>Rank</th><th>Team</th><th>Wins</th><th>Losses</th><th>Ties</th><th>Points</th></tr><tr><td>1</td><td>Carolina Hurricanes</td><td>49</td><td>20</td><td>8</td><td>106</td></tr><tr><td>2</td><td>New York Rangers</td><td>50</td><td>21</td><td>6</td><td>106</td></tr><tr><td>3</td><td>Pittsburgh Penguins</td><td>43</td><td>23</td><td>11</td><td>97</td></tr><tr><td>4</td><td>Washington Capitals</td><td>43</td><td>23</td><td>10</td><td>96</td></tr><tr><td>5</td><td>New York Islanders</td><td>35</td><td>31</td><td>10</td><td>80</td></tr><tr><td>6</td><td>Columbus Blue Jackets</td><td>35</td><td>36</td><td>6</td><td>76</td></tr><tr><td>7</td><td>New Jersey Devils</td><td>27</td><td>42</td><td>7</td><td>61</td></tr><tr><td>8</td><td>Philadelphia Flyers</td><td>23</td><td>43</td><td>11</td><td>57</td></tr></table><h3>Atlantic Division Standings</h3><table><tr><th>Rank</th><th>Team</th><th>Wins</th><th>Losses</th><th>Ties</th><th>Points</th></tr><tr><td>1</td><td>Florida Panthers</td><td>55</td><td>15</td><td>6</td><td>116</td></tr><tr><td>2</td><td>Toronto Maple Leafs</td><td>51</td><td>20</td><td>6</td><td>108</td></tr><tr><td>3</td><td>Tampa Bay Lightning</td><td>46</td><td>22</td><td>8</td><td>100</td></tr><tr><td>4</td><td>Boston Bruins</td><td>47</td><td>24</td><td>5</td><td>99</td></tr><tr><td>5</td><td>Detroit Red Wings</td><td>30</td><td>37</td><td>10</td><td>70</td></tr><tr><td>6</td><td>Buffalo Sabres</td><td>29</td><td>38</td><td>11</td><td>69</td></tr><tr><td>7</td><td>Ottawa Senators</td><td>29</td><td>41</td><td>7</td><td>65</td></tr><tr><td>8</td><td>Montreal Canadiens</td><td>20</td><td>46</td><td>11</td><td>51</td></tr></table><h3>Western Conference Standings</h3><table><tr><th>Rank</th><th>Team</th><th>Wins</th><th>Losses</th><th>Ties</th><th>Points</th></tr><tr><td>1</td><td>Colorado Avalanche</td><td>55</td><td>15</td><td>6</td><td>116</td></tr><tr><td>2</td><td>Calgary Flames</td><td>47</td><td>20</td><td>10</td><td>104</td></tr><tr><td>3</td><td>Minnesota Wild</td><td>48</td><td>21</td><td>7</td><td>103</td></tr><tr><td>4</td><td>St. Louis Blues</td><td>46</td><td>20</td><td>11</td><td>103</td></tr><tr><td>5</td><td>Edmonton Oilers</td><td>44</td><td>26</td><td>6</td><td>94</td></tr><tr><td>6</td><td>Nashville Predators</td><td>44</td><td>28</td><td>5</td><td>93</td></tr><tr><td>7</td><td>Los Angeles Kings</td><td>41</td><td>27</td><td>10</td><td>92</td></tr><tr><td>8</td><td>Dallas Stars</td><td>43</td><td>28</td><td>5</td><td>91</td></tr><tr><td>9</td><td>Vegas Golden Knights</td><td>41</td><td>31</td><td>5</td><td>87</td></tr><tr><td>10</td><td>Vancouver Canucks</td><td>38</td><td>28</td><td>11</td><td>87</td></tr><tr><td>11</td><td>Winnipeg Jets</td><td>35</td><td>31</td><td>11</td><td>81</td></tr><tr><td>12</td><td>Anaheim Ducks</td><td>30</td><td>34</td><td>14</td><td>74</td></tr><tr><td>13</td><td>San Jose Sharks</td><td>30</td><td>34</td><td>12</td><td>72</td></tr><tr><td>14</td><td>Chicago Blackhawks</td><td>25</td><td>40</td><td>11</td><td>61</td></tr><tr><td>15</td><td>Seattle Kraken</td><td>25</td><td>44</td><td>6</td><td>56</td></tr><tr><td>16</td><td>Arizona Coyotes</td><td>22</td><td>49</td><td>5</td><td>49</td></tr></table><h3>Eastern Conference Standings</h3><table><tr><th>Rank</th><th>Team</th><th>Wins</th><th>Losses</th><th>Ties</th><th>Points</th></tr><tr><td>1</td><td>Florida Panthers</td><td>55</td><td>15</td><td>6</td><td>116</td></tr><tr><td>2</td><td>Toronto Maple Leafs</td><td>51</td><td>20</td><td>6</td><td>108</td></tr><tr><td>3</td><td>Carolina Hurricanes</td><td>49</td><td>20</td><td>8</td><td>106</td></tr><tr><td>4</td><td>New York Rangers</td><td>50</td><td>21</td><td>6</td><td>106</td></tr><tr><td>5</td><td>Tampa Bay Lightning</td><td>46</td><td>22</td><td>8</td><td>100</td></tr><tr><td>6</td><td>Boston Bruins</td><td>47</td><td>24</td><td>5</td><td>99</td></tr><tr><td>7</td><td>Pittsburgh Penguins</td><td>43</td><td>23</td><td>11</td><td>97</td></tr><tr><td>8</td><td>Washington Capitals</td><td>43</td><td>23</td><td>10</td><td>96</td></tr><tr><td>9</td><td>New York Islanders</td><td>35</td><td>31</td><td>10</td><td>80</td></tr><tr><td>10</td><td>Columbus Blue Jackets</td><td>35</td><td>36</td><td>6</td><td>76</td></tr><tr><td>11</td><td>Detroit Red Wings</td><td>30</td><td>37</td><td>10</td><td>70</td></tr><tr><td>12</td><td>Buffalo Sabres</td><td>29</td><td>38</td><td>11</td><td>69</td></tr><tr><td>13</td><td>Ottawa Senators</td><td>29</td><td>41</td><td>7</td><td>65</td></tr><tr><td>14</td><td>New Jersey Devils</td><td>27</td><td>42</td><td>7</td><td>61</td></tr><tr><td>15</td><td>Philadelphia Flyers</td><td>23</td><td>43</td><td>11</td><td>57</td></tr><tr><td>16</td><td>Montreal Canadiens</td><td>20</td><td>46</td><td>11</td><td>51</td></tr></table>
    """
    send_email(example_subject, example_html)


