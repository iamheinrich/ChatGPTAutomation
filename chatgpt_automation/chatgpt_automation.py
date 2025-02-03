from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import socket
import threading
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
import logging
import platform
import pyperclip
from chatgpt_automation.chromedriver_manager import ChromeDriverManager
# TODO: Replace autoit with a solution that's cross-platform compatible. autoit is only used for upload_file_for_prompt
# import autoit
import subprocess
from typing import List, Optional, Dict, Any
# Configure logging
logging.basicConfig(filename='chatgpt_automation.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')


class ChatGPTLocators:
    MSG_BOX_INPUT = (By.CSS_SELECTOR, 'textarea#prompt-textarea')
    MSG_BOX_INPUT2 = (By.TAG_NAME, 'textarea')
    MSG_BOX_INPUT3 = (By.ID, 'prompt-textarea')

    SEND_MSG_BTN = (By.XPATH, "//*[contains(@data-testid, 'send-button')]")

    GPT4_FILE_INPUT = (By.XPATH, '//input[@class="hidden"]')
    
    WEB_SEARCH_INPUT = (By.XPATH, '/html/body/div[1]/div[2]/main/div[1]/div[1]/div/div/div/div/article[1]/div/div/div/div/div/div/div/div/div[1]')
    WEB_SEARCH_OUTPUT = (By.XPATH, '/html/body/div[1]/div[2]/main/div[1]/div[1]/div/div/div/div/article[1]/div/div/div/div/div/div/div/div/div[2]')

    # WEB_SEARCH_BTN = (By.XPATH, '/html/body/div[1]/div[2]/main/div[1]/div[1]/div/div[2]/div/div/div/div[4]/form/div/div/div/div/div[2]/div[1]/div[3]/div/span/button')
    WEB_SEARCH_BTN = (By.CSS_SELECTOR, "#composer-background > div.mb-2.mt-1.flex.items-center.justify-between.sm\:mt-5 > div.flex.gap-x-1\.5.text-token-text-primary > div:nth-child(2) > div > span > button")
    
    SHOW_WEB_SEARCH_SOURCES_BTN = (By.CSS_SELECTOR, 'body > div.flex.h-full.w-full.flex-col > div > div.relative.flex.h-full.w-full.flex-row.overflow-hidden > div.relative.flex.h-full.max-w-full.flex-1.flex-col.overflow-hidden > main > div.composer-parent.flex.h-full.flex-col.focus-visible\:outline-0 > div.flex-1.overflow-hidden.\@container\/thread > div > div > div > div > article:nth-child(3) > div > div > div.group\/conversation-turn.relative.flex.w-full.min-w-0.flex-col.agent-turn > div.flex-col.gap-1.md\:gap-3 > div.flex.max-w-full.flex-col.flex-grow > div > div > div > div.absolute.h-\[60px\] > button')
    
    WEB_SEARCH_SOURCES_CITATIONS = (By.CSS_SELECTOR, 'body > div.flex.h-full.w-full.flex-col > div > div.z-\[1\].flex-shrink-0.overflow-x-hidden.bg-token-sidebar-surface-primary.max-md\:\!w-0 > div > div > section > div:nth-child(2) > div > div:nth-child(1) > div.flex.flex-col.px-3.py-2')
    WEB_SEARCH_SOURCES_MORE = (By.CSS_SELECTOR, 'body > div.flex.h-full.w-full.flex-col > div > div.z-\[1\].flex-shrink-0.overflow-x-hidden.bg-token-sidebar-surface-primary.max-md\:\!w-0 > div > div > section > div:nth-child(2) > div > div:nth-child(2) > div.flex.flex-col.px-3.py-2')
    
    # The button to click to come to the end of the conversation
    WEB_SEARCH_CURSOR_POINTER = (By.CSS_SELECTOR, 'body > div.flex.h-full.w-full.flex-col > div > div.relative.flex.h-full.w-full.flex-row.overflow-hidden > div.relative.flex.h-full.max-w-full.flex-1.flex-col.overflow-hidden > main > div.composer-parent.flex.h-full.flex-col.focus-visible\:outline-0 > div.flex-1.overflow-hidden.\@container\/thread > div > div > div > div > button')
    
    # Card that shows an error message
    ERROR_CARD = (By.CSS_SELECTOR, 'body > div.flex.h-full.w-full.flex-col > div > div.relative.flex.h-full.w-full.flex-row.overflow-hidden > div.relative.flex.h-full.max-w-full.flex-1.flex-col.overflow-hidden > main > div.composer-parent.flex.h-full.flex-col.focus-visible\:outline-0 > div.flex-1.overflow-hidden.\@container\/thread > div > div > div > div > article:nth-child(3) > div > div > div.group\/conversation-turn.relative.flex.w-full.min-w-0.flex-col.agent-turn > div > div.flex.max-w-full.flex-col.flex-grow > div')
    
    CHAT_GPT_CONVERSION = (By.CSS_SELECTOR, 'div.text-base')
    CHAT_GPT_RESPONSE_WEB_SEARCH = (By.CSS_SELECTOR, 'body > div.flex.h-full.w-full.flex-col > div > div.relative.flex.h-full.w-full.flex-row.overflow-hidden > div.relative.flex.h-full.max-w-full.flex-1.flex-col.overflow-hidden > main > div.composer-parent.flex.h-full.flex-col.focus-visible\:outline-0 > div.flex-1.overflow-hidden.\@container\/thread > div > div > div > div > article:nth-child(3) > div > div > div.group\/conversation-turn.relative.flex.w-full.min-w-0.flex-col.agent-turn > div.flex-col.gap-1.md\:gap-3 > div.flex.max-w-full.flex-col.flex-grow > div > div > div')
    CHAT_GPT_RESPONSE_WEB_SEARCH_2 = (By.CSS_SELECTOR, 'body > div.flex.h-full.w-full.flex-col > div > div.relative.flex.h-full.w-full.flex-row.overflow-hidden > div.relative.flex.h-full.max-w-full.flex-1.flex-col.overflow-hidden > main > div.composer-parent.flex.h-full.flex-col.focus-visible\:outline-0 > div.flex-1.overflow-hidden.\@container\/thread > div > div > div > div > article:nth-child(3) > div > div > div.group\/conversation-turn.relative.flex.w-full.min-w-0.flex-col.agent-turn > div > div.flex.max-w-full.flex-col.flex-grow > div.min-h-8.text-message.flex.w-full.flex-col.items-end.gap-2.whitespace-normal.break-words.text-start.\[\.text-message\+\&\]\:mt-5 > div > div')
    REGENERATE_BTN = (By.CSS_SELECTOR, 'button[as="button"]')

    FIRST_DELETE_BTN = (By.CSS_SELECTOR, 'button[data-state="closed"]')
    SECOND_DELETE_BTN = (
        By.CSS_SELECTOR, 'div[role="menuitem"].text-token-text-error')
    THIRD_DELETE_BTN = (By.CSS_SELECTOR, 'button.btn.btn-danger[as="button"]')

    RECYCLE_BTN = (By.CSS_SELECTOR,
                   'button.p-1.hover\\:text-token-text-primary:nth-child(2)')
    DELETE_CONFIRM_BTN = (By.CSS_SELECTOR, 'button.btn.relative.btn-danger')

    NEW_CHAT_BTN = (By.CSS_SELECTOR, 'button.text-token-text-primary')

    LOGIN_BTN = (By.XPATH, '//button[//div[text()="Log in"]]')
    CONTINUE_BTN = (By.XPATH, '//button[text()="Continue"]')
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")

    CHATGPT_SWITCH_HOVER_BTN = (By.CSS_SELECTOR, 'div[aria-haspopup="menu"]')
    CHAT_GPT_SWITCH_TO_4 = (By.XPATH, '//div[text()="GPT-4"]')
    CHAT_GPT_SWITCH_TO_3 = (By.XPATH, '//div[contains(text(), "GPT-3.5")]')
    CHAT_GPT_SWITCH_TO_4O = (By.XPATH, '//div[text()="GPT-4o"]')
    UPGRADE_TO_PLUS_BTN = (
        By.XPATH, '//div[contains(text(), "Upgrade to Plus")]')

    COPY_LAST_RESPONSE_BTN = (
        By.CSS_SELECTOR, '.rounded-lg.text-token-text-secondary.hover\\:bg-token-main-surface-secondary')

    LOGIN_WITH_GMAIL_BTN = (
        By.CSS_SELECTOR, 'form[data-provider="google"] button[data-provider="google"]')
    GMAIL_BTN = (By.XPATH, '//div[@data-email="{}"]')

    GMAIL_INPUT = (By.CSS_SELECTOR, 'input[type="email"][id="identifierId"]')
    GMAIL_NEXT_BTN = (By.ID, 'identifierNext')
    GMAIL_PASSWORD_INPUT = (
        By.CSS_SELECTOR, 'input[type="password"][name="password"]')
    GMAIL_PASSWORD_NEXT_BTN = (By.ID, 'passwordNext')
    ADD_NEW_GMAIL_BTN = (By.XPATH, '//li[contains(.,"Use another account")]')

    RESPONSE_DIV = (By.CLASS_NAME, "markdown")

    FILE_UPLOAD_BTN = (By.XPATH, "//button[@aria-disabled='false']")
    FILE_UPLOAD_BTN_SELECT_SUB_MENU = (
        By.XPATH, "//div[@role='menuitem' and contains(text(), 'Upload from computer')]")

    ERROR_DIALOG_CLASS_NAME = (By.CSS_SELECTOR, ".toast-root")

    UPLOADING_PROCESS = (By.TAG_NAME, 'circle')


class ChatGPTAutomation:
    class DelayTimes:
        CONSTRUCTOR_DELAY = 4
        SEND_PROMPT_DELAY = 12
        UPLOAD_FILE_DELAY = 6
        RETURN_LAST_RESPONSE_DELAY = 1
        OPEN_NEW_CHAT_DELAY = 6
        DEL_CURRENT_CHAT_OPEN_MENU_DELAY = 2
        DEL_CURRENT_CHAT_AFTER_DELETE_DELAY = 3
        DEL_CURRENT_CHAT_BEFORE_OPEN_NEW_CHAT_DELAY = 3
        CHECK_RESPONSE_STATUS_DELAY = 4
        LOGIN_USING_GMAIL_CLICK_DELAY = 4
        GMAIL_SELECT_DELAY = 15
        AFTER_LOGIN_CLICK_DELAY = 3
        ADD_GMAIL_CLICK_DELAY = 3
        GMAIL_NEXT_CLICK_DELAY = 5
        GMAIL_PASSWORD_NEXT_CLICK_DELAY = 11

    def __init__(self, chrome_path=None, chrome_driver_path=None, username: str = None, password: str = None, user_data_dir=None):
        """
        This constructor automates the following steps:
        1. Open a Chrome browser with remote debugging enabled at a specified URL.
        2. Prompt the user to complete the log-in/registration/human verification, if required.
        3. Connect a Selenium WebDriver to the browser instance after human verification is completed.

        :param chrome_path: file path to chrome.exe (ex. C:\\Users\\User\\...\\chromedriver.exe)
        :param chrome_driver_path: file path to chrome.exe (ex. C:\\Users\\User\\...\\chromedriver.exe)
        """
        self.user_data_dir = user_data_dir
        self.lock = threading.Lock()
        if chrome_path is None:
            chrome_path = self.get_chrome_path()
            if chrome_path is None:
                raise FileNotFoundError("Unable to automatically find the Chrome path. "
                                        "Please provide the path to the Chrome executable.")

        if chrome_driver_path is None:
            try:
                chrome_driver_path = ChromeDriverManager().install()
            except Exception as e:
                raise RuntimeError(
                    f"An unexpected error occurred while installing ChromeDriver: {e}")

        # chrome_path = f'"{chrome_path}" {user_data_dir}'
        self.chrome_path = chrome_path
        self.chrome_driver_path = chrome_driver_path

        self.url = r"https://chatgpt.com"
        free_port = self.find_available_port()
        self.launch_chrome_with_remote_debugging(free_port, self.url)
        # self.wait_for_human_verification()
        self.driver = self.setup_webdriver(free_port)

        self.username = username
        self.password = password

        time.sleep(self.DelayTimes.CONSTRUCTOR_DELAY)

    def check_login_page(self) -> bool:
        """
        Checks whether the login page is accessible by attempting to locate the login button.

        :return: True if the login button is found, indicating the presence of the login page; False otherwise.
        """
        return bool(self.driver.find_elements(*ChatGPTLocators.LOGIN_BTN))
    
    def activate_web_search(self):
        """
        Activates the web search feature in ChatGPT if it's not already activated.
        Checks the button's state to determine if web search is already active.

        Raises:
            WebDriverException: If there is an issue interacting with the web elements or sending the prompt.
        """
        try:
            # First check if web search button exists and is clickable
            wait = WebDriverWait(self.driver, 3)
            web_search_btn = wait.until(
                EC.element_to_be_clickable(ChatGPTLocators.WEB_SEARCH_BTN)
            )
            
            # Check if web search is already activated by checking the button's aria-pressed attribute
            aria_pressed = web_search_btn.get_attribute("aria-pressed")
            if aria_pressed == "true":
                print("Web search is already activated")
                return
                
            # Web search is not activated, proceed with activation
            web_search_btn.click()
            print("Web search activated")
            
            # Short wait for UI update
            time.sleep(0.5)
                
        except Exception as e:
            logging.error(f"Failed to activate web search: {e}")
            raise WebDriverException(f"Error activating web search: {e}")
    
    def show_web_search_sources(self):
        """
        Shows the web search sources in ChatGPT by clicking the "Sources" button.

        Raises:
            WebDriverException: If there is an issue interacting with the web elements or sending the prompt.
        """
        try:
            print("Attempting to click the show web search sources button")
            self.driver.find_element(*ChatGPTLocators.SHOW_WEB_SEARCH_SOURCES_BTN).click()
        except Exception as e:
            logging.error(f"Failed to show web search sources: {e}")
            raise WebDriverException(f"Error showing web search sources: {e}")

    
    def get_links_from_sources(self,locator):
        """
        Retrieves all href links from <a> tags nested within the sidebar of sources section of the sources sidebar.

        :param xpath: XPath of the sources sidebar container. Is either the "More" or "Citations" section.
        :return: List of all href links of the citations.
        """
        try:
            print(f"Attempting to locate {locator}")

            # Locate the container using the provided XPath
            container = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(locator)
            )
            print("Container found in the DOM.")

            # Ensure the container is visible
            WebDriverWait(self.driver, 20).until(
                EC.visibility_of(container)
            )
            print("Container is visible.")

            # Find all <a> tags recursively within the container
            all_links = container.find_elements(By.XPATH, ".//a")
            print(f"Found {len(all_links)} <a> tags in the container.")

            # Extract href attributes from the <a> tags
            hrefs = [link.get_attribute("href") for link in all_links if link.get_attribute("href")]
            print(f"Extracted {len(hrefs)} hrefs from the <a> tags.")

            return hrefs

        except Exception as e:
            logging.error(f"Error extracting links: {e}")
            print(f"Error extracting links: {e}")
            return []

    def get_all_citations(self):
        return self.get_links_from_sources(ChatGPTLocators.WEB_SEARCH_SOURCES_CITATIONS)
    
    def get_more_links(self):
        return self.get_links_from_sources(ChatGPTLocators.WEB_SEARCH_SOURCES_MORE)

    def login_using_gamil(self, email: str = None):
        if email is None:
            if self.username is None:
                raise Exception(
                    "You must pass the email in username field when you create the class")
            else:
                email = self.username

        login_btn = self.driver.find_element(*ChatGPTLocators.LOGIN_BTN)
        login_btn.click()

        time.sleep(self.DelayTimes.AFTER_LOGIN_CLICK_DELAY)

        gmail_login_btn = self.driver.find_element(
            *ChatGPTLocators.LOGIN_WITH_GMAIL_BTN)
        gmail_login_btn.click()

        time.sleep(self.DelayTimes.LOGIN_USING_GMAIL_CLICK_DELAY)

        gmail_btn = self.driver.find_element(
            ChatGPTLocators.GMAIL_BTN[0], ChatGPTLocators.GMAIL_BTN[1].format(email))
        gmail_btn.click()

        time.sleep(self.DelayTimes.GMAIL_SELECT_DELAY)

    def login(self, username: str = None, password: str = None):
        if username is None:
            if self.username is None or self.password is None:
                raise Exception(
                    "You must pass the username and password in the first step of creating the class or pass them when calling the function.")
            else:
                username = self.username
                password = self.password

        login_btn = self.driver.find_element(*ChatGPTLocators.LOGIN_BTN)
        login_btn.click()

        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(ChatGPTLocators.USERNAME_INPUT)
        ).send_keys(username)

        self.driver.find_element(*ChatGPTLocators.CONTINUE_BTN).click()

        pass_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(ChatGPTLocators.PASSWORD_INPUT)
        )
        pass_input.send_keys(password)
        pass_input.send_keys(Keys.ENTER)

    def find_available_port(self):
        """
        Finds and returns an available port number on the local machine.
        It does this by creating a temporary socket, binding it to an ephemeral port,
        and then closing the socket to free the port for use.

        Returns:
            available_port (int): The available port number found.

        Raises:
            Exception: If the function fails to find an available port due to a socket error.
        """
        try:
            # Create a socket object using IPv4 addressing and TCP
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                # Bind the socket to any available address on the machine ('') and port 0
                # The OS will then automatically assign an available ephemeral port
                s.bind(('', 0))

                # Set socket options - SO_REUSEADDR allows the socket to be bound to an address
                # that is already in use, which is useful for avoiding socket errors
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

                # Retrieve the port number assigned by the OS
                available_port = s.getsockname()[1]

                # Log the found available port
                logging.info(f"Available port found: {available_port}")

                # Return the found port
                return available_port

        except socket.error as e:
            # Log the error in case of a socket exception
            logging.error(f"Failed to find an available port: {e}")

            # Raise a new exception for the calling code to handle
            raise Exception("Failed to find an available port") from e

    def launch_chrome_with_remote_debugging(self, port, url):
        """
        Launches a new Chrome browser instance with remote debugging enabled. This method allows for
        Selenium WebDriver to connect to a pre-existing Chrome session.

        Args:
            port (int): The port number to use for remote debugging.
            url (str): The URL to navigate to when the browser opens.

        Raises:
            RuntimeError: If there is an error in launching the Chrome browser.
        """

        def open_chrome():
            try:
                # Construct the Chrome launch arguments
                args = [
                    self.chrome_path,
                    f"--remote-debugging-port={port}",
                ]

                # Only include user-data-dir if it's provided
                if self.user_data_dir:
                    args.append(f"--user-data-dir={self.user_data_dir}")

                # Include URL as the final argument
                args.append(url)

                # Construct the command to launch Chrome with specified debugging port and URL

               # Execute the command in the system shell for windows
                if platform.system() == "Windows":
                    chrome_cmd = f"{self.chrome_path} --remote-debugging-port={
                        port} --user-data-dir={self.user_data_dir} {url}"
                    os.system(chrome_cmd)
                else:
                    # For mac and linux use subprocess
                    subprocess.Popen(args)

            except Exception as e:
                # Log and raise an exception if there's an error in launching Chrome
                logging.error(f"Failed to launch Chrome: {e}")
                raise RuntimeError(
                    f"Failed to launch Chrome with remote debugging: {e}")

        try:
            # Create a new thread to run the Chrome launch command
            chrome_thread = threading.Thread(target=open_chrome)
            # Start the thread
            chrome_thread.start()
        except Exception as e:
            # Log and raise an exception if there's an error in starting the thread
            logging.error(f"Failed to start Chrome launch thread: {e}")
            raise RuntimeError(
                f"Failed to start thread for launching Chrome: {e}")

    def setup_webdriver(self, port):
        """
        Initializes and returns a Selenium WebDriver instance that is connected to an existing
        Chrome browser with remote debugging enabled. This method is crucial for controlling
        an already opened browser instance.

        Args:
            port (int): The port number on which the remote debugging of the Chrome browser is enabled.

        Returns:
            webdriver.Chrome: An instance of Chrome WebDriver connected to the existing browser session.

        Raises:
            WebDriverException: If there is an issue initializing the WebDriver.
        """

        try:
            # Setting up Chrome options for WebDriver
            chrome_options = webdriver.ChromeOptions()
            # Specifying the address for the remote debugging
            chrome_options.binary_location = self.chrome_driver_path
            chrome_options.add_experimental_option(
                "debuggerAddress", f"127.0.0.1:{port}")
            # Initializing the Chrome WebDriver with the specified options
            driver = webdriver.Chrome(
                self.chrome_driver_path, options=chrome_options)
            return driver
        except Exception as e:
            # Log the exception if WebDriver initialization fails
            logging.error(f"Failed to initialize WebDriver: {e}")
            # Raising a WebDriverException to indicate failure in WebDriver setup
            raise WebDriverException(f"Error initializing WebDriver: {e}")

    def check_if_element_exists(self, locator):
        return bool(self.driver.find_elements(*locator))

    def send_prompt_to_chatgpt(self, prompt):
        """
        Sends a message to ChatGPT via the web interface and waits for a response. This function
        automates the process of entering a prompt into the ChatGPT input box and triggering the send action.

        Args:
            prompt (str): The message or prompt to be sent to ChatGPT.

        Raises:
            WebDriverException: If there is an issue interacting with the web elements or sending the prompt.
        """

        try:
            # Wait for the input box to be visible and clickable
            input_box = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(ChatGPTLocators.MSG_BOX_INPUT3)
            )
            input_box.click()
            self.type_in_selected_area(prompt, input_box)
            input_box.send_keys(Keys.ENTER)
            time.sleep(self.DelayTimes.SEND_PROMPT_DELAY)
        except (ElementNotInteractableException, TimeoutException) as e:
            logging.error("Element not interactable or timeout occurred.")
            raise WebDriverException(f"Error sending prompt to ChatGPT: {e}")
        except Exception as e:
            logging.error(f"Failed to send prompt to ChatGPT: {e}")
            raise WebDriverException(f"Error sending prompt to ChatGPT: {e}")

    # TODO: Rewrite the function using a package that is not autoit. Autoit is only available on windows.
    # def upload_file_for_prompt(self, file_name, retry_count=1):
    #     """
    #     Uploads a file to ChatGPT via the web interface. This function automates the process of
    #     selecting a file for upload through the ChatGPT's file input element.

    #     Args:
    #         file_name (str): The name of the file to be uploaded.
    #         retry_count (int): Number of times to retry the upload in case of an error.

    #     Raises:
    #         FileNotFoundError: If the specified file does not exist in the current working directory.
    #         WebDriverException: If there is an issue interacting with the file upload element on the web page.
    #     """

    #     def check_file_exists(file_path):
    #         if not os.path.exists(file_path):
    #             raise FileNotFoundError(
    #                 f"The file '{file_path}' does not exist.")

    #     def perform_file_upload(file_path):
    #         try:
    #             file_input = self.driver.find_element(
    #                 *ChatGPTLocators.FILE_UPLOAD_BTN)
    #             file_input.click()
    #             time.sleep(2)
    #             self.driver.find_element(
    #                 *ChatGPTLocators.FILE_UPLOAD_BTN_SELECT_SUB_MENU).click()
    #             time.sleep(2)
    #             autoit.control_send("[CLASS:#32770]", "Edit1", file_path)
    #             autoit.control_click("[CLASS:#32770]", "Button1")
    #         except NoSuchElementException:
    #             raise Exception(
    #                 "You must be using GPT-4 to upload files. To switch, you can use the 'switch_model' function!"
    #             )
    #         except Exception as e:
    #             logging.error(e)
    #             raise e
    #         time.sleep(self.DelayTimes.UPLOAD_FILE_DELAY)

    #     def verify_upload(file_name):
    #         if self.check_dialog_error():
    #             raise WebDriverException(
    #                 "Error dialog detected during file upload.")
    #         print(file_name)
    #         if not self.check_upload_success(file_name):
    #             raise WebDriverException(
    #                 "File upload was not successful. The file is not listed on the page.")

    #     check_file_exists(file_name)

    #     for attempt in range(1, retry_count + 1):
    #         try:
    #             logging.info(f"Attempt {attempt} to upload file.")
    #             perform_file_upload(file_name)
    #             time.sleep(self.DelayTimes.UPLOAD_FILE_DELAY)

    #             verify_upload(file_name.split('\\')[-1])
    #             logging.info("File upload successful.")
    #             return  # Exit the function if the upload is successful
    #         except WebDriverException as e:
    #             logging.error(f"Upload attempt {attempt} failed: {e}")
    #             if attempt == retry_count:
    #                 logging.error("All retry attempts failed.")
    #                 raise WebDriverException(f"All retry attempts failed: {e}")

    #     raise WebDriverException(
    #         "File upload failed after all retry attempts.")
    

    def return_chatgpt_conversation(self):
        """
        :return: returns a list of items, even items are the submitted questions (prompts) and odd items are chatgpt response
        """
        print("Returning chatgpt conversation")
        elements = self.driver.find_elements(
            *ChatGPTLocators.CHAT_GPT_CONVERSION)
        del elements[::2]
        print("Elements found: ",elements)
        chat_texts = [element.text for element in elements]
        print("Chatgpt conversation returned")
        return chat_texts
    
    def check_for_error_card(self) -> bool:
        """
        Checks if an error card is present in the response.

        Returns:
            bool: True if an error card is found, False otherwise
        """
        try:
            self.driver.find_element(*ChatGPTLocators.ERROR_CARD)
            print("Error card detected in response")
            return True
        except NoSuchElementException:
            return False

    def wait_for_response_completion(self, timeout: int = 30) -> bool:
        """
        Waits for the response to be complete by checking for the Sources button.
        Adds a short delay after finding the button to ensure response is fully rendered.
        
        Args:
            timeout: Maximum time to wait in seconds
            
        Returns:
            bool: True if response is complete, False if timeout occurred
        """
        try:
            wait = WebDriverWait(self.driver, timeout)
            
            # Wait for sources button to appear
            wait.until(
                EC.presence_of_element_located(ChatGPTLocators.SHOW_WEB_SEARCH_SOURCES_BTN)
            )
            
            # Add a short delay to ensure response is fully rendered
            time.sleep(3)
            return True
            
        except TimeoutException:
            print(f"Response completion timeout after {timeout} seconds")
            return False

    def get_response_from_web_search(self) -> List[str]:
        """
        Extracts text from all nested <p> child tags under the web search response from ChatGPT.
        Handles cases where text is wrapped in other tags like <strong>.
        For long responses, handles the cursor pointer button that appears at the bottom.

        Returns:
            list: A list of strings containing the combined text of all <p> tags.

        Raises:
            WebDriverException: If no response is generated from the web search or if there's an error extracting text.
            NoSuchElementException: If neither response element is found on the page.
            TimeoutException: If the response does not appear within the specified timeout.
        """
        try:
            print("Waiting for response to complete...")
            if not self.wait_for_response_completion(timeout=30):
                error_msg = "Timeout waiting for response to complete"
                logging.error(error_msg)
                raise TimeoutException(error_msg)

            print("Response complete, extracting content...")
            wait = WebDriverWait(self.driver, 5)

            # Try to find either of the response elements
            parent_element = None
            try:
                print("Locating response container...")
                # Use a compound condition to wait for either element
                parent_element = wait.until(
                    lambda driver: (
                        driver.find_element(*ChatGPTLocators.CHAT_GPT_RESPONSE_WEB_SEARCH) or 
                        driver.find_element(*ChatGPTLocators.CHAT_GPT_RESPONSE_WEB_SEARCH_2)
                    )
                )
                print("Response container found.")
            except (TimeoutException, NoSuchElementException):
                error_msg = "No response element was found on the page."
                logging.error(error_msg)
                raise NoSuchElementException(error_msg)

            # After finding the parent, check for cursor pointer
            try:
                cursor_pointer = self.driver.find_element(*ChatGPTLocators.WEB_SEARCH_CURSOR_POINTER)
                if cursor_pointer.is_displayed():
                    print("Cursor pointer found, clicking to scroll to bottom")
                    cursor_pointer.click()
                    time.sleep(0.5)  # Short wait after click
            except NoSuchElementException:
                print("No cursor pointer found, proceeding with response extraction")

            print("Finding all text elements within the parent element.")
            # Look for both paragraphs and list items
            text_elements = parent_element.find_elements(By.CSS_SELECTOR, "p, li, div.prose")
            
            # If no direct elements found, try to find any elements with text content
            if not text_elements:
                print("No direct elements found, searching all descendants for text...")
                text_elements = parent_element.find_elements(By.XPATH, ".//*[normalize-space(text())]")

            if not text_elements:
                error_msg = "No text elements found in the web search response."
                logging.error(error_msg)
                raise NoSuchElementException(error_msg)
            
            print(f"Number of text elements found: {len(text_elements)}")

            print("Extracting and cleaning text from each element.")
            extracted_texts = []
            for element in text_elements:
                try:
                    # Try text property first as it's faster
                    text = element.text
                    if not text:
                        text = element.get_attribute('textContent')
                    if text:
                        cleaned_text = text.strip()
                        if cleaned_text:  # Only add non-empty strings
                            extracted_texts.append(cleaned_text)
                except Exception as e:
                    logging.warning(f"Failed to extract text from element: {e}")
                    continue

            print(f"Extracted texts: {extracted_texts}")

            if not extracted_texts:
                error_msg = "No text content was found in the web search response."
                logging.error(error_msg)
                raise WebDriverException(error_msg)

            return extracted_texts

        except (TimeoutException, NoSuchElementException) as e:
            # Re-raise these specific exceptions
            raise
        except Exception as e:
            error_msg = f"Error while extracting text from web search: {e}"
            logging.error(error_msg)
            raise WebDriverException(error_msg)

    def save_conversation(self, file_name, search_type="custom"):
        """
        Saves the entire conversation from the ChatGPT interface into a text file. The conversation is formatted
        with prompts and responses, separated by a custom delimiter.

        Args:
            file_name (str): The name of the file where the conversation will be saved.
            search_type (str): The type of search that was performed. Can be "custom" or "web_search".

        Raises:
            IOError: If there is an issue writing to the file.
            IndexError: If the conversation elements are not found or are in an unexpected format.
        """

        try:
            directory_name = "conversations"
            if not os.path.exists(directory_name):
                os.makedirs(directory_name)

            delimiter = "----------------------------------------"
            if search_type == "web_search":
                chatgpt_conversation = self.get_response_from_web_search()
                assert isinstance(chatgpt_conversation, list), f"chatgpt_conversation is expected to be a list but is{type(chatgpt_conversation)}"

            else:
                chatgpt_conversation = self.return_chatgpt_conversation()
                del chatgpt_conversation[::2]

            with open(os.path.join(directory_name, file_name), "a") as file:
                for i in range(0, len(chatgpt_conversation)):
                    print("Adding the following to the file: ", chatgpt_conversation[i])
                    file.write(f"{chatgpt_conversation[i]}\n\n{delimiter}\n\n")
                    print("Added delimiter")

        except FileNotFoundError as e:
            logging.error(f"File not found: {e}")
            raise
        except PermissionError as e:
            logging.error(f"Permission denied: {e}")
            raise
        except IOError as e:
            logging.error(f"IO error occurred: {e}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error in saving conversation: {e}")
            raise
        
    
    def return_last_response(self):
        """
        Retrieves the text of the last ChatGPT response from a web interface using Selenium WebDriver.

        The function uses a specific CSS selector to locate the last ChatGPT response on the page. It then
        triggers a click action on a button within that container to copy the response text to the clipboard.
        The text is retrieved from the clipboard and returned. Error handling and logging are implemented
        to capture any issues during the execution of the function.

        :return: The text of the last ChatGPT response as a string, or an error message if an exception occurs.
        """

        try:
            response = self.driver.find_elements(
                *ChatGPTLocators.RESPONSE_DIV)[-1]

            return response.text

        except NoSuchElementException:
            # Handle the case where the element is not found
            logging.error('Element not found in return_last_response')
            return "Element not found."
        except Exception as e:
            # Handle any other exceptions
            logging.error(
                f'Unexpected error in return_last_response: {str(e)}')
            return f"An unexpected error occurred: {str(e)}"

    def return_last_response_md(self):
        try:
            copy_btns = self.driver.find_elements(
                *ChatGPTLocators.COPY_LAST_RESPONSE_BTN)
            if copy_btns:
                copy_btns[-3].click()
                time.sleep(self.DelayTimes.RETURN_LAST_RESPONSE_DELAY)
                return pyperclip.paste()
            else:
                logging.warning("No copy button found.")
                return "No copy button found."

        except Exception as e:
            logging.error(
                f"Unexpected error in return_last_response_md: {str(e)}")
            return f"An unexpected error occurred: {str(e)}"

    def wait_for_human_verification(self):
        """
        Pauses the automation process and waits for the user to manually complete tasks such as log-in
        or human verification, which are not automatable. The function repeatedly prompts the user until
        they confirm the completion of the manual task.

        Returns:
            None

        Raises:
            SystemExit: If an unrecoverable input error occurs, indicating a problem with the system or environment.
        """
        with self.lock:
            print(
                "You need to manually complete the log-in or the human verification if required.")

            while True:
                try:
                    user_input = input(
                        "Enter 'y' if you have completed the log-in or the human verification, or 'n' to check again: ").lower()
                except EOFError:
                    # Print error message and exit the program in case of an End-Of-File condition on input
                    print("Error reading input. Exiting the program.")
                    # Exiting the program due to input error
                    raise SystemExit("Failed to read user input.")

                # Check the user's input and act accordingly
                if user_input == 'y':
                    print("Continuing with the automation process...")
                    break  # Break the loop to continue with automation
                elif user_input == 'n':
                    print("Waiting for you to complete the human verification...")
                    # Waiting for a specified time before asking again
                    time.sleep(5)
                else:
                    # Handle invalid input
                    print("Invalid input. Please enter 'y' or 'n'.")

    def write_last_answer_custom_file(self, filename):
        """
        Retrieves the latest response from ChatGPT and writes it to a specified file. The file is saved
        with UTF-8 encoding to support a wide range of characters.

        Parameters:
            filename (str): The name of the file (including path if necessary) where the last response will be saved.

        Returns:
            None: The function does not return any value.

        Raises:
            IOError: If there is an issue writing to the file.
        """

        try:
            answer = self.return_last_response()
            with open(filename, "w", encoding="utf8") as file:
                file.write(answer)
            print(f"Last answer saved in the file: {filename}")

        except FileNotFoundError as e:
            logging.error(f"File not found: {e}")
            raise
        except PermissionError as e:
            logging.error(f"Permission denied: {e}")
            raise
        except IOError as e:
            logging.error(f"IO error occurred: {e}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error in writing last answer: {e}")
            raise

    def open_new_chat(self):
        """
        Navigates to the ChatGPT page using the WebDriver, effectively starting a new chat session.
        Ensures the page is fully loaded before returning.

        Raises:
            WebDriverException: If there is an issue navigating to the ChatGPT page.
        """
        try:
            # Print the URL being opened for debugging
            print(f"Opening URL: {self.url.rstrip('/') + '/'}")
            # Navigate to the ChatGPT URL to start a new chat session
            self.driver.get(self.url + "/")
            
            # Wait for the page to be fully loaded and interactive
            wait = WebDriverWait(self.driver, 10)
            wait.until(
                EC.presence_of_element_located(ChatGPTLocators.MSG_BOX_INPUT3)
            )
            
            # Additional wait for any animations or dynamic content
            time.sleep(2)
            
            # Print confirmation message
            print("New chat opened and ready")
            
        except Exception as e:
            # Log the exception if navigation fails
            logging.error(f"Failed to open new chat: {e}")
            # Raising a WebDriverException to indicate failure in navigation
            raise WebDriverException(f"Error opening new chat: {e}")

    def del_current_chat(self):
        """
        Deletes the current chat session in the ChatGPT interface. This function interacts with specific UI elements
        to trigger the deletion process of the active chat conversation.

        Handling:
            - If a timeout occurs (elements not found in time), it attempts to open a new chat session.
            - Any other exceptions trigger a retry by opening a new chat session.

        Raises:
            WebDriverException: If there are issues in deleting the chat or in navigating to start a new chat.
        """
        try:
            # Wait and click the first delete button
            del_chat_btn1 = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (ChatGPTLocators.FIRST_DELETE_BTN[0], ChatGPTLocators.FIRST_DELETE_BTN[1]))
            )
            del_chat_btn1.click()
            # Wait for UI response
            time.sleep(self.DelayTimes.DEL_CURRENT_CHAT_OPEN_MENU_DELAY)

            # Wait and click the second delete button
            del_chat_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (ChatGPTLocators.SECOND_DELETE_BTN[0], ChatGPTLocators.SECOND_DELETE_BTN[1]))
            )
            del_chat_btn.click()

            # Wait and click the third delete button to confirm deletion
            del_chat_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (ChatGPTLocators.THIRD_DELETE_BTN[0], ChatGPTLocators.THIRD_DELETE_BTN[1]))
            )
            del_chat_btn.click()

            print("Current chat deleted")
            # Wait for the chat to be completely deleted
            time.sleep(self.DelayTimes.DEL_CURRENT_CHAT_AFTER_DELETE_DELAY)

        except TimeoutException:
            # Handle timeout exception when elements are not found within the specified time
            print("Timeout: Elements not found within the specified time.")
            try:
                self.open_new_chat()
            except Exception as e:
                logging.error(f"Failed to open new chat after timeout: {e}")
                raise WebDriverException(
                    f"Error navigating to start a new chat after timeout: {e}")

        except Exception as e:
            # Handle any other exceptions that might occur
            logging.error(f"Error encountered while deleting chat: {e}")
            try:
                time.sleep(
                    self.DelayTimes.DEL_CURRENT_CHAT_BEFORE_OPEN_NEW_CHAT_DELAY)
                self.open_new_chat()
            except Exception as e:
                logging.error(f"Failed to open new chat after error: {e}")
                raise WebDriverException(
                    f"Error navigating to start a new chat after deletion error: {e}")

    def check_error(self, regenerate=False):
        """
        Checks if there is an error message displayed on the webpage, indicating a problem with response generation.

        This method attempts to locate a specific error message element on the webpage using an XPath expression.
        If an error is found and the 'regenerate' flag is True, it triggers a response regeneration.
        Logs the occurrence of an error for debugging purposes.

        :param regenerate: A boolean flag indicating whether to regenerate the response if an error is found.
        :return: True if an error is detected, False otherwise.
        """
        try:
            # Locate the error message element using XPath
            error_element = self.driver.find_element(By.XPATH,
                                                     "//div[@class='mb-3 text-center text-xs' and text()='There was an error generating a response']")
            logging.info("Error detected: Responding error!")

            # Regenerate response if the flag is set
            if regenerate:
                self.regenerate()

            return True
        except NoSuchElementException:
            # Log that no error was found
            logging.info("No error detected.")
            return False
        except Exception as e:
            # Log any other exceptions that may occur
            logging.error(f"An unexpected error occurred: {e}")
            return False

    def check_response_status(self):
        """
        Continuously checks the status of the response on the webpage.

        This method loops indefinitely, checking for two conditions:
        1. If there is an error on the page, indicated by the check_error method.
        2. If the 'send' button is available, indicating that the response is ready to be sent.

        The method waits for a set interval before rechecking the conditions.

        :return: False if an error is detected, True if the response is ready to be sent.
        """
        while True:
            # Check for errors on the page
            if self.check_error(False):
                logging.info("Response Status: Error detected.")
                return False

            try:
                # Check if the 'send' button is available, indicating the response is ready
                self.driver.find_element(*ChatGPTLocators.SEND_MSG_BTN)
                logging.info("Response Status: Ready to send.")
                return True
            except NoSuchElementException:
                # If 'send' button is not found, continue the loop
                pass

            # Log and wait before checking again
            logging.info("Responding...")
            time.sleep(self.DelayTimes.CHECK_RESPONSE_STATUS_DELAY)

    def switch_model(self, model_name: str):
        """
        Switches between different ChatGPT models in the application's user interface.

        :param model_name: A float representing the desired ChatGPT model version.
                        Supported values are 3.5 and 4.
        :return: None
        :raises: Exception if an unsupported model_name is provided.
        """
        menu_element = self.driver.find_element(
            *ChatGPTLocators.CHATGPT_SWITCH_HOVER_BTN)

        # Hover over the menu to activate it
        menu_element.click()

        # Wait for the submenu to be visible (adjust timeout as needed)
        if model_name == "4":
            submenu_locator = ChatGPTLocators.CHAT_GPT_SWITCH_TO_4
            try:
                # Check for the UPGRADE_TO_PLUS_BTN
                self.driver.find_element(*ChatGPTLocators.UPGRADE_TO_PLUS_BTN)
                raise Exception(
                    "You must upgrade your ChatGPT account to plus")
            except NoSuchElementException:
                pass
        elif model_name == "3.5":
            submenu_locator = ChatGPTLocators.CHAT_GPT_SWITCH_TO_3
        elif model_name == "4o":
            submenu_locator = ChatGPTLocators.CHAT_GPT_SWITCH_TO_4O
            try:
                # Check for the UPGRADE_TO_PLUS_BTN
                self.driver.find_element(*ChatGPTLocators.UPGRADE_TO_PLUS_BTN)
                raise Exception(
                    "You must upgrade your ChatGPT account to plus")
            except NoSuchElementException:
                pass
        else:
            raise Exception(
                "To switch between models, you need to set the 'model_name' to 3.5 or 4")

        submenu_element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(submenu_locator))

        # Click on the submenu item
        submenu_element.click()

    @staticmethod
    def get_chrome_path() -> str:
        try:
            if platform.system() == 'Windows':
                for path in [
                    r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
                    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
                ]:
                    if os.path.isfile(path):
                        return r'"{}"'.format(path)

            elif platform.system() == 'Darwin':  # macOS
                path = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
                if os.path.isfile(path):
                    return path

            elif platform.system() == 'Linux':
                paths = [
                    '/usr/bin/google-chrome',
                    '/usr/local/bin/google-chrome'
                ]
                for path in paths:
                    if os.path.isfile(path):
                        return path

        except PermissionError as e:
            logging.error(f"Permission error when trying to find Chrome: {e}")
        except OSError as e:
            logging.error(f"OS error when trying to find Chrome: {e}")
        except Exception as e:
            logging.error(f"Unexpected error when trying to find Chrome: {e}")

        return None

    # def check_verify_page(self):
    #     try:
    #         element = self.driver.find_element(By.XPATH, f'//*[contains(text(), "Verify you are human")]')
    #         return True
    #     except NoSuchElementException:
    #         return False
    #     except Exception as e:
    #         logging.error(f"unexpected error: {e}")
    #         raise Exception(e)
    #
    # def pass_verify(self):
    #     try:
    #         checkbox = driver.find_element(By.CSS_SELECTOR, 'input[type="checkbox"]')
    #         if not checkbox.is_selected():
    #             checkbox.click()
    #
    #         time.sleep(15)
    #     except NoSuchElementException:
    #         logging.error("Check Box for human verify doesn't find!")
    #         raise Exception("Check Box for human verify doesn't find!")

    def quit(self):
        """
        Closes the browser and terminates the WebDriver session.

        This method first attempts to close the current window of the browser using the `close` method.
        Then it calls the `quit` method to effectively end the entire WebDriver session.
        Error handling is implemented to catch any exceptions that might occur during this process.
        """
        try:
            # Attempt to close the current browser window
            print("Closing the browser...")
            self.driver.close()

            # Terminate the WebDriver session
            self.driver.quit()
            logging.info(
                "Browser closed successfully and WebDriver session terminated.")
        except Exception as e:
            # Log any exceptions that occur during the quit process
            logging.error(f"An error occurred while closing the browser: {e}")

    def gmail_login_setup(self, email: str = None, password: str = None):
        """
        Automates the Gmail login process within the ChatGPT web interface using Selenium WebDriver. This method handles the
        authentication process by entering provided Gmail credentials or using those stored in the class instance.

        The function follows a specific sequence of steps to navigate through the ChatGPT login interface and to input the 
        Gmail credentials. If two-factor authentication (2FA) or human verification is required, the function prompts the 
        user to complete these steps manually.

        Args:
            email (str, optional): The email address for the Gmail account. If not provided, the class instance's email is used.
            password (str, optional): The password for the Gmail account. If not provided, the class instance's password is used.

        Workflow:
        1. Validates the presence of email and password.
        2. Navigates through the ChatGPT login interface, clicking relevant buttons to reach the Gmail login section.
        3. Enters the email and password into the Gmail login form.
        4. Handles additional steps such as 2FA or human verification if they are triggered during login.

        Raises:
            Exception: If neither email nor password is provided either through function arguments or stored in the class instance.

        Note:
        - This function assumes that the WebDriver (`self.driver`) and specific locators (`ChatGPTLocators`) are already initialized.
        - The user may need to manually complete 2FA or human verification steps if they are prompted by Gmail.
        """
        if (email is None or password is None) and (self.username is None or self.password is None):
            raise Exception(
                "you must pass email and password in function params or when you create the class...")
        elif (email is None or password is None) and (self.username is not None or self.password is not None):
            email = self.username
            password = self.password

        login_btn = self.driver.find_element(*ChatGPTLocators.LOGIN_BTN)
        login_btn.click()

        time.sleep(self.DelayTimes.AFTER_LOGIN_CLICK_DELAY)

        gmail_login_btn = self.driver.find_element(
            *ChatGPTLocators.LOGIN_WITH_GMAIL_BTN)
        gmail_login_btn.click()

        time.sleep(self.DelayTimes.LOGIN_USING_GMAIL_CLICK_DELAY)

        add_gmail_btn = self.driver.find_element(
            *ChatGPTLocators.ADD_NEW_GMAIL_BTN)
        add_gmail_btn.click()

        time.sleep(self.DelayTimes.ADD_GMAIL_CLICK_DELAY)

        gmail_input = self.driver.find_element(*ChatGPTLocators.GMAIL_INPUT)
        gmail_input.send_keys(email)

        next_btn = self.driver.find_element(*ChatGPTLocators.GMAIL_NEXT_BTN)
        next_btn.click()

        time.sleep(self.DelayTimes.GMAIL_NEXT_CLICK_DELAY)

        password_input = self.driver.find_element(
            *ChatGPTLocators.GMAIL_PASSWORD_INPUT)
        password_input.send_keys(password)

        next_btn = self.driver.find_element(
            *ChatGPTLocators.GMAIL_PASSWORD_NEXT_BTN)
        next_btn.click()

        time.sleep(self.DelayTimes.GMAIL_PASSWORD_NEXT_CLICK_DELAY)

        try:
            self.driver.find_element(*ChatGPTLocators.MSG_BOX_INPUT)
            print("Login completed!")
        except:
            print("you need manually complete the 2FA or human verification...")
            with self.lock:
                while True:
                    try:
                        user_input = input(
                            "Enter 'y' if you have completed the log-in or the human verification, or 'n' to check again: ").lower()
                    except EOFError:
                        # Print error message and exit the program in case of an End-Of-File condition on input
                        print("Error reading input. Exiting the program.")
                        # Exiting the program due to input error
                        raise SystemExit("Failed to read user input.")

                    # Check the user's input and act accordingly
                    if user_input == 'y':
                        print(
                            "Authentication Completed!\nContinuing with the automation process...")
                        break  # Break the loop to continue with automation
                    elif user_input == 'n':
                        print("Waiting for you to complete the human verification...")
                        # Waiting for a specified time before asking again
                        time.sleep(5)
                    else:
                        # Handle invalid input
                        print("Invalid input. Please enter 'y' or 'n'.")

    def type_in_selected_area(self, text: str, element):
        for char in text:
            if char == "\n":
                element.send_keys(Keys.SHIFT + Keys.ENTER)
            else:
                element.send_keys(char)

    def check_dialog_error(self):
        try:
            error_dialog = self.driver.find_element(
                *ChatGPTLocators.ERROR_DIALOG_CLASS_NAME)
        except NoSuchElementException:
            return False
        return True

    def check_upload_success(self, file_name):
        try:
            self.driver.find_element(By.XPATH, f"//div[text()='{file_name}']")
        except NoSuchElementException:
            return False
        return True
