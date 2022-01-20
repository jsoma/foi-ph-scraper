{
 "cells": [
  {
   "cell_type": "markdown",
   "id": "c051a56c",
   "metadata": {},
   "source": [
    "# Philippines' Freedom of Information website scraper and analysis\n",
    "\n",
    "**(Data from September 2016-January 19 and ongoing)**\n",
    "\n",
    "Below scrapes and processes requests data from the Philippines' Freedom of Information website **(www.foi.gov.ph)** and combining the same with an **existing file** of **older FOI requests from 2016.** \n",
    "\n",
    "The goal is to create a single database of these requests (which we will do in a separate notebook) and analyze them such as:\n",
    "\n",
    "Which agency received the most number of requests?\n",
    "\n",
    "How many requests had been denied/approved?\n",
    "\n",
    "What type of requests are most common?\n",
    "\n",
    "Some background: The FOI website is in compliance with Executive Order No. 2, Series of 2016 by President Rodrigo Duterte that institutionalized freedom of information in the Executive branch of government."
   ]
  },
  {
   "cell_type": "markdown",
   "id": "99cb2d6e",
   "metadata": {},
   "source": [
    "## Do your imports"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "f300e9ca",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "/Users/prinzmagtulis/.pyenv/versions/3.10.0/lib/python3.10/site-packages/pandas/compat/__init__.py:124: UserWarning: Could not import the lzma module. Your installed Python is incomplete. Attempting to use lzma compression will result in a RuntimeError.\n",
      "  warnings.warn(msg)\n"
     ]
    }
   ],
   "source": [
    "import pandas as pd\n",
    "\n",
    "import time\n",
    "import requests\n",
    "import re\n",
    "\n",
    "from selenium import webdriver\n",
    "from selenium.webdriver.common.keys import Keys\n",
    "from selenium.webdriver.support.ui import Select\n",
    "from selenium.webdriver.support.ui import WebDriverWait\n",
    "from selenium.webdriver.support import expected_conditions as EC\n",
    "from selenium.webdriver.common.by import By\n",
    "\n",
    "from webdriver_manager.chrome import ChromeDriverManager\n",
    "\n",
    "from bs4 import BeautifulSoup"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "1cff23bb",
   "metadata": {},
   "source": [
    "## Open a new browser to be automatically controlled by Selenium"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "9f61c1a4",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "\n",
      "\n",
      "====== WebDriver manager ======\n",
      "Could not get version for google-chrome with the any command: /Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome --version\n",
      "Current google-chrome version is UNKNOWN\n",
      "Get LATEST chromedriver version for UNKNOWN google-chrome\n",
      "Driver [/Users/prinzmagtulis/.wdm/drivers/chromedriver/mac64/97.0.4692.71/chromedriver] found in cache\n",
      "/var/folders/01/dz49lpcd4qq_yksvf114xzfc0000gn/T/ipykernel_3385/1503906442.py:1: DeprecationWarning: executable_path has been deprecated, please pass in a Service object\n",
      "  driver = webdriver.Chrome(ChromeDriverManager().install())\n"
     ]
    }
   ],
   "source": [
    "driver = webdriver.Chrome(ChromeDriverManager().install())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "b9e486a2",
   "metadata": {},
   "outputs": [],
   "source": [
    "driver.get(\"https://www.foi.gov.ph/requests\")"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "1952c205",
   "metadata": {},
   "source": [
    "Note: That is the part of the website supposedly containing all FOI requests."
   ]
  },
  {
   "cell_type": "markdown",
   "id": "54141a3c",
   "metadata": {},
   "source": [
    "## Start locating and isolating elements\n",
    "\n",
    "Some methods are:\n",
    "\n",
    "By.TAG\n",
    "\n",
    "By.CLASS_NAME\n",
    "\n",
    "By.ID\n",
    "\n",
    "By.XPATH\n",
    "\n",
    "By.CSS_SELECTOR"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "id": "e0470198",
   "metadata": {},
   "outputs": [],
   "source": [
    "tabs = driver.find_elements(By.CLASS_NAME, \"col-xxs-12 col-xs-12 col-sm-8\")"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "994bc1b4",
   "metadata": {},
   "source": [
    "## Actual scraping"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "60803cff",
   "metadata": {},
   "source": [
    "Now comes the main part: interacting with the pages and setting Selenium to scrape each page. We then put scraped information in a **list of dictionaries** and then into a **single data frame.** \n",
    "\n",
    "Kudos to my friend, Vincent, for some help in using **CSS_SELECTOR** as a locator since I'm not familiar with it."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "id": "478b4c80",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n",
      "Reading a page\n"
     ]
    }
   ],
   "source": [
    "dataset = []\n",
    "while True:\n",
    "    try:\n",
    "        print('Reading a page')\n",
    "        WebDriverWait(driver, 4).until(\n",
    "            EC.presence_of_element_located((By.CSS_SELECTOR, \".col-xxs-12.col-xs-12.col-sm-8\"))\n",
    "        )\n",
    "        tabs = driver.find_elements(By.CSS_SELECTOR, \".col-xxs-12.col-xs-12.col-sm-8\")\n",
    "        for tab in tabs:\n",
    "            try:\n",
    "                all_div = tab.find_elements(By.CSS_SELECTOR, '.component-panel')\n",
    "            except:\n",
    "                break\n",
    "            for div in all_div[1:]:\n",
    "                data={}\n",
    "                data ['agency'] = div.find_element(By.TAG_NAME, 'span').text\n",
    "                data ['date'] = div.find_element(By.TAG_NAME, 'p').get_attribute('title')\n",
    "                data ['title'] = div.find_element(By.TAG_NAME, 'h4').text\n",
    "                data ['status'] = div.find_element(By.TAG_NAME, 'label').text\n",
    "                data ['purpose'] = div.find_elements(By.TAG_NAME, 'span')[2].text\n",
    "                data ['period_covered'] = div.find_elements(By.TAG_NAME, 'span')[3].text\n",
    "                data ['link'] = div.find_element(By.TAG_NAME, 'a').get_attribute('href')\n",
    "                dataset.append(data)\n",
    "    except:\n",
    "        break\n",
    "\n",
    "    try:\n",
    "        driver.find_element(By.XPATH, \"/html/body/section/div/div/div/div[2]/div/div/div/a\").click()\n",
    "    except:\n",
    "        print(\"Nothing more.\")\n",
    "        break"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "cf532a2a",
   "metadata": {},
   "source": [
    "## Generate your (first) data frame\n",
    "\n",
    "This is now all pandas."
   ]
  },
  {
   "cell_type": "markdown",
   "id": "951c2fa0",
   "metadata": {},
   "source": [
    "So, some caveats:\n",
    "\n",
    "First, the **ALL REQUESTS** tab apparently only contains data for about the past 40 or so days (in this case from **December 7, 2021**). Hence, we can only scrape until that level-- that represent only or **about 6%** of what the website says as **\"93,373 requests\"**."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "id": "99836c2f",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>agency</th>\n",
       "      <th>date</th>\n",
       "      <th>title</th>\n",
       "      <th>status</th>\n",
       "      <th>purpose</th>\n",
       "      <th>period_covered</th>\n",
       "      <th>link</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>PSA</td>\n",
       "      <td>January 20, 2022</td>\n",
       "      <td>Copy of PSA Birth certificate (Mary Anne Robis...</td>\n",
       "      <td>PENDING</td>\n",
       "      <td>Clarification for Misrepresentation of COC</td>\n",
       "      <td>01/20/1950 - 01/20/2022</td>\n",
       "      <td>https://www.foi.gov.ph/requests/aglzfmVmb2ktcG...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>DOST-ASTI</td>\n",
       "      <td>January 20, 2022</td>\n",
       "      <td>Daily Rainfall Data surrounding Mt. Banahaw fr...</td>\n",
       "      <td>PENDING</td>\n",
       "      <td>Research and Instruction</td>\n",
       "      <td>01/01/2010 - 12/31/2020</td>\n",
       "      <td>https://www.foi.gov.ph/requests/aglzfmVmb2ktcG...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>DSWD</td>\n",
       "      <td>January 20, 2022</td>\n",
       "      <td>SAP beneficiaries of San Roque Northern Samar</td>\n",
       "      <td>PENDING</td>\n",
       "      <td>Research on Good Governance</td>\n",
       "      <td>04/01/2020 - 12/31/2021</td>\n",
       "      <td>https://www.foi.gov.ph/requests/aglzfmVmb2ktcG...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>DA</td>\n",
       "      <td>January 20, 2022</td>\n",
       "      <td>Goat and Carabao Dispersal San Roque Northern ...</td>\n",
       "      <td>PENDING</td>\n",
       "      <td>Research on Good Governance</td>\n",
       "      <td>01/01/2013 - 12/31/2021</td>\n",
       "      <td>https://www.foi.gov.ph/requests/aglzfmVmb2ktcG...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>SSS</td>\n",
       "      <td>January 20, 2022</td>\n",
       "      <td>SSS sickness and EC benefits positive COVID-19</td>\n",
       "      <td>PENDING</td>\n",
       "      <td>Follow on SSS sickness application</td>\n",
       "      <td>09/24/2021 - 10/10/2021</td>\n",
       "      <td>https://www.foi.gov.ph/requests/aglzfmVmb2ktcG...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>...</th>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>6414</th>\n",
       "      <td>DOH</td>\n",
       "      <td>December 07, 2021</td>\n",
       "      <td>VAXCERT</td>\n",
       "      <td>SUCCESSFUL</td>\n",
       "      <td>Follow up request</td>\n",
       "      <td>11/15/2021 - 12/07/2021</td>\n",
       "      <td>https://www.foi.gov.ph/requests/aglzfmVmb2ktcG...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>6415</th>\n",
       "      <td>DOH</td>\n",
       "      <td>December 07, 2021</td>\n",
       "      <td>Vax Certificate</td>\n",
       "      <td>SUCCESSFUL</td>\n",
       "      <td>Request for vax certificate</td>\n",
       "      <td>12/01/2021 - 12/07/2021</td>\n",
       "      <td>https://www.foi.gov.ph/requests/aglzfmVmb2ktcG...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>6416</th>\n",
       "      <td>OWWA</td>\n",
       "      <td>December 07, 2021</td>\n",
       "      <td>OFW DOLE-AKAP Cash Assistance</td>\n",
       "      <td>SUCCESSFUL</td>\n",
       "      <td>Cash Releasing of DOLE AKAP cash assistance</td>\n",
       "      <td>11/13/2021 - 12/07/2021</td>\n",
       "      <td>https://www.foi.gov.ph/requests/aglzfmVmb2ktcG...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>6417</th>\n",
       "      <td>DOH</td>\n",
       "      <td>December 07, 2021</td>\n",
       "      <td>Urgent! Vaccination Certification For Travel</td>\n",
       "      <td>SUCCESSFUL</td>\n",
       "      <td>For Travel on December 9</td>\n",
       "      <td>07/26/2021 - 08/23/2021</td>\n",
       "      <td>https://www.foi.gov.ph/requests/aglzfmVmb2ktcG...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>6418</th>\n",
       "      <td>PCAARRD</td>\n",
       "      <td>December 07, 2021</td>\n",
       "      <td>Stream flow Data in the Province of Cavite</td>\n",
       "      <td>DENIED</td>\n",
       "      <td>National Irrigation Administration - National ...</td>\n",
       "      <td>12/06/2015 - 12/06/2021</td>\n",
       "      <td>https://www.foi.gov.ph/requests/aglzfmVmb2ktcG...</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "<p>6419 rows × 7 columns</p>\n",
       "</div>"
      ],
      "text/plain": [
       "         agency               date  \\\n",
       "0           PSA   January 20, 2022   \n",
       "1     DOST-ASTI   January 20, 2022   \n",
       "2          DSWD   January 20, 2022   \n",
       "3            DA   January 20, 2022   \n",
       "4           SSS   January 20, 2022   \n",
       "...         ...                ...   \n",
       "6414        DOH  December 07, 2021   \n",
       "6415        DOH  December 07, 2021   \n",
       "6416       OWWA  December 07, 2021   \n",
       "6417        DOH  December 07, 2021   \n",
       "6418    PCAARRD  December 07, 2021   \n",
       "\n",
       "                                                  title      status  \\\n",
       "0     Copy of PSA Birth certificate (Mary Anne Robis...     PENDING   \n",
       "1     Daily Rainfall Data surrounding Mt. Banahaw fr...     PENDING   \n",
       "2         SAP beneficiaries of San Roque Northern Samar     PENDING   \n",
       "3     Goat and Carabao Dispersal San Roque Northern ...     PENDING   \n",
       "4        SSS sickness and EC benefits positive COVID-19     PENDING   \n",
       "...                                                 ...         ...   \n",
       "6414                                            VAXCERT  SUCCESSFUL   \n",
       "6415                                    Vax Certificate  SUCCESSFUL   \n",
       "6416                      OFW DOLE-AKAP Cash Assistance  SUCCESSFUL   \n",
       "6417       Urgent! Vaccination Certification For Travel  SUCCESSFUL   \n",
       "6418         Stream flow Data in the Province of Cavite      DENIED   \n",
       "\n",
       "                                                purpose  \\\n",
       "0            Clarification for Misrepresentation of COC   \n",
       "1                              Research and Instruction   \n",
       "2                           Research on Good Governance   \n",
       "3                           Research on Good Governance   \n",
       "4                    Follow on SSS sickness application   \n",
       "...                                                 ...   \n",
       "6414                                  Follow up request   \n",
       "6415                        Request for vax certificate   \n",
       "6416        Cash Releasing of DOLE AKAP cash assistance   \n",
       "6417                           For Travel on December 9   \n",
       "6418  National Irrigation Administration - National ...   \n",
       "\n",
       "               period_covered  \\\n",
       "0     01/20/1950 - 01/20/2022   \n",
       "1     01/01/2010 - 12/31/2020   \n",
       "2     04/01/2020 - 12/31/2021   \n",
       "3     01/01/2013 - 12/31/2021   \n",
       "4     09/24/2021 - 10/10/2021   \n",
       "...                       ...   \n",
       "6414  11/15/2021 - 12/07/2021   \n",
       "6415  12/01/2021 - 12/07/2021   \n",
       "6416  11/13/2021 - 12/07/2021   \n",
       "6417  07/26/2021 - 08/23/2021   \n",
       "6418  12/06/2015 - 12/06/2021   \n",
       "\n",
       "                                                   link  \n",
       "0     https://www.foi.gov.ph/requests/aglzfmVmb2ktcG...  \n",
       "1     https://www.foi.gov.ph/requests/aglzfmVmb2ktcG...  \n",
       "2     https://www.foi.gov.ph/requests/aglzfmVmb2ktcG...  \n",
       "3     https://www.foi.gov.ph/requests/aglzfmVmb2ktcG...  \n",
       "4     https://www.foi.gov.ph/requests/aglzfmVmb2ktcG...  \n",
       "...                                                 ...  \n",
       "6414  https://www.foi.gov.ph/requests/aglzfmVmb2ktcG...  \n",
       "6415  https://www.foi.gov.ph/requests/aglzfmVmb2ktcG...  \n",
       "6416  https://www.foi.gov.ph/requests/aglzfmVmb2ktcG...  \n",
       "6417  https://www.foi.gov.ph/requests/aglzfmVmb2ktcG...  \n",
       "6418  https://www.foi.gov.ph/requests/aglzfmVmb2ktcG...  \n",
       "\n",
       "[6419 rows x 7 columns]"
      ]
     },
     "execution_count": 7,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "df = pd.DataFrame(dataset)\n",
    "df"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "id": "c23996a2",
   "metadata": {},
   "outputs": [],
   "source": [
    "df.to_csv(\"foi1.csv\", index=False)\n",
    "pd.read_csv(\"foi1.csv\")"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.10.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
