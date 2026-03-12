# evalify_app/tests_selenium.py
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class SeleniumTests(StaticLiveServerTestCase):
    """Test suite using Selenium to verify frontend pages."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        service = Service(ChromeDriverManager().install())
        cls.driver = webdriver.Chrome(service=service)
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def test_home_page_loads(self):
        """Verify home page loads with correct title."""
        self.driver.get(self.live_server_url + '/')
        self.assertIn('Evalify - Smart Assessment Platform', self.driver.title)

    def test_signup_page_loads(self):
        """Verify signup page loads correctly."""
        self.driver.get(self.live_server_url + '/signup/')
        self.assertEqual(self.driver.title, 'Evalify - Create Account')
        # Check presence of key elements
        self.assertTrue(self.driver.find_element(By.CSS_SELECTOR, 'input[placeholder*="profile name"]').is_displayed())
        self.assertTrue(self.driver.find_element(By.CSS_SELECTOR, 'input[placeholder*="email"]').is_displayed())

    def test_signin_page_loads(self):
        """Verify signin page loads correctly."""
        self.driver.get(self.live_server_url + '/signin/')
        self.assertEqual(self.driver.title, 'Evalify - Sign In')
        # Check heading
        heading = self.driver.find_element(By.TAG_NAME, 'h2')
        self.assertIn('Sign In To Continue', heading.text)

    def test_navigation_from_home(self):
        """Test that buttons on home page lead to correct auth pages."""
        self.driver.get(self.live_server_url + '/')

        # Click SIGN UP button (button with class 'btn-signup')
        signup_btn = self.driver.find_element(By.CSS_SELECTOR, '.btn-signup')
        signup_btn.click()
        self.assertIn('/signup/', self.driver.current_url)
        self.assertEqual(self.driver.title, 'Evalify - Create Account')

        # Go back to home
        self.driver.back()

        # Click SIGN IN button (button with class 'btn-signin')
        signin_btn = self.driver.find_element(By.CSS_SELECTOR, '.btn-signin')
        signin_btn.click()
        self.assertIn('/signin/', self.driver.current_url)
        self.assertEqual(self.driver.title, 'Evalify - Sign In')

    def test_navigation_between_auth_pages(self):
        """Test links between signup and signin pages work."""
        # From signup page, go to signin
        self.driver.get(self.live_server_url + '/signup/')
        login_link = self.driver.find_element(By.CSS_SELECTOR, '.login-link a')
        login_link.click()
        self.assertIn('/signin/', self.driver.current_url)

        # From signin page, go back to signup
        signup_link = self.driver.find_element(By.CSS_SELECTOR, '.login-link a')
        signup_link.click()
        self.assertIn('/signup/', self.driver.current_url)