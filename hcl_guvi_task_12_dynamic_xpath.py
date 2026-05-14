"""
GUVI HCL TASK - 12
This task is going to validate your usage of Dynamic XPATH on the web application -https://www.guvi.in/

    1) Go to the URL - https://www.guvi.in/
    2) Refer to the image given below :-
    3) Relative XPath
        • Given an element which is underlined in Red in color, find the "parent" element,
        find the first "child" element.
        • Locate the second sibling (If any).
        • Select the parent element of an element with the attribute "href".

    4) Axes:
        • Find all ancestor elements
        • Locate all following siblings
        • Select all preceding elements
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By

# ==================================================================================================#
# CONSTANTS                                                                                        #
# ==================================================================================================#

GUVI_BASE_URL = "https://www.guvi.in/"

# Navbar link names — match the red-underlined elements in the reference image.
# Note: "Our Solutions" was renamed to "Our Products" on the live GUVI homepage.
NAV_BAR_LINK_TEXT_LIST = [
    "LIVE Classes",  # [0] First navbar item
    "Courses",  # [1]
    "Practice",  # [2]
    "Resources",  # [3]
    "Our Products",  # [4] Previously "Our Solutions"
    "Login + Sign up",  # [5] Combined Login & Sign up section
]
# XPath for the repeating dropdown nav elements
NAVBAR_ELEMENTS_COMMON_XPATH_STR = "(//div[@class='⭐️f6lmuc-0 group relative cursor-pointer'])"

# XPath for the Login + Sign up section
LOGIN_SIGNUP_XPATH_STR = "(//div[@class='⭐️3hk5qd-0 flex gap-5 z-50'])[1]"

# ==================================================================================================#
# HELPER FUNCTIONS                                                                                 #
# ==================================================================================================#

def generate_rel_xpath_and_find_element(driver, navbar_el_name, relation, **kwargs):
    """
    Builds a mapping of navbar element name → its base XPath string.
    Maps a relation name to its XPath axis extension string.
    Builds a dynamic XPath for a given navbar element and relation type,
    then locates and returns the matching WebElement(s).

    Args:
        driver          : Selenium WebDriver instance.
        navbar_el_name  : Text label of the target navbar element.
        relation        : Relationship type string (e.g. "parent", "first child").
        **kwargs:
            href (bool) : If True, restricts the base XPath to elements with @href.

    Returns:
        WebElement       — for single-element relations (parent, child, sibling).
        list[WebElement] — for "all ..." relations (ancestors, siblings, preceding).
        None             — if the element is not found or an error occurs.
    """

    xpath_str_with_href = "//a[normalize-space(text())='" + navbar_el_name + "' and @href]"
    navbar_el_xpath_str = "//a[normalize-space(text())='" + navbar_el_name + "']"
    xpath_extension = ''
    relation = relation.lower()

    # Create a dictionary with mapping of navbar element name → its base XPath string.
    navbar_el_xpath_dict = {NAV_BAR_LINK_TEXT_LIST[i]: NAVBAR_ELEMENTS_COMMON_XPATH_STR + "[" + str(i + 1) + "]" for i
                            in
                            range(len(NAV_BAR_LINK_TEXT_LIST[:5]))}
    navbar_el_xpath_dict[NAV_BAR_LINK_TEXT_LIST[-1]] = LOGIN_SIGNUP_XPATH_STR

    # Build the base XPath
    if 'href' in kwargs and kwargs["href"] == True:
        xpath_str = xpath_str_with_href
    elif "all" in relation:
        xpath_str = navbar_el_xpath_dict[navbar_el_name]
    else:
        xpath_str = navbar_el_xpath_dict[navbar_el_name]

    # Mapping of relation labels → XPath axis extension
    match relation:
        case "parent":
            xpath_extension = "/parent::*"
        case "first child":
            xpath_extension = "/child::*[1]"
        case "second sibling":
            xpath_extension = "/following-sibling::*[2]"
        case "all ancestor elements":
            xpath_extension = "/ancestor::*"
        case "all following siblings":
            xpath_extension = "/following-sibling::*"
        case "all preceding elements":
            xpath_extension = "/preceding::*"
        case _:
            xpath_extension = ""

    # Add the XPath axis extension and generate full XPath
    full_xpath = xpath_str + xpath_extension

    try:
        if "all" in relation:

            # Axes related queries: find_elements returns a list (may be empty)
            print(f"AXES XPATH ---> {full_xpath}")
            elements = driver.find_elements(By.XPATH, full_xpath)
            return elements
        elif "href" in kwargs and kwargs["href"] == True:

            # href-related queries: single element, check enabled only
            print(f"Relative XPATH ---> {full_xpath}")
            element = driver.find_element(By.XPATH, full_xpath)
            if element.is_enabled():
                return element
        else:

            # Standard relative XPath: single element, check visible + enabled
            print(f"Relative XPATH ---> {full_xpath}")
            element = driver.find_element(By.XPATH, full_xpath)
            if element.is_displayed() and element.is_enabled():
                return element

    except Exception as e:
        print(f"No {relation} found for '{navbar_el_name}' element(s)! → Error: {e}")
        return None


def print_element(element, el_name, relation):
    """
    Prints the tag name, visible text, href (if present), and innerHTML
    of a single WebElement.

    Args:
        element  : WebElement to inspect (or None if not found).
        el_name  : Name of the navbar element (used in error messages).
        relation : Human-readable relation label (printed in uppercase).
    """
    try:
        tag = element.tag_name
        text = element.text.strip() or "(no text)"
        href = element.get_attribute("href")
        relation = relation.upper()
        inner_html = element.get_attribute("innerHTML")

        # Include href in the output only if the element actually has one
        if href is not None:
            print(f"\t{relation} -> <{tag} href: {href}>  text: {text!r}")
        else:
            print(f"\t{relation} -> <{tag}> text: {text!r}")

        # Print innerHTML
        print(f"Inner HTML: \n\t{inner_html}\n")

    except Exception as e:
        print(f"{relation.upper()} for '{el_name}' element not found! → Error: {e}")
        print()


def print_elements(elements, el_name, relation):
    """
    Prints the index, tag name, visible text, and innerHTML for each element
    in a list of WebElements.

    Args:
        elements : list[WebElement] returned by an axes query.
        el_name  : Name of the source navbar element (used in header).
        relation : Human-readable relation label (printed in uppercase).
    """
    print(f"\t{relation.upper()} — {len(elements)} element(s) found:")
    for i, el in enumerate(elements, 1):
        try:
            tag = el.tag_name
            text = el.text.strip() or "(no text)"
            inner_html = el.get_attribute("innerHTML")
            print(f"\t[{i}] <{tag}>  text: {text!r}")
            print(f"\tInner HTML: \n\t{inner_html}\n")
        except Exception:
            print(f"\t[{i}] (stale or unavailable)")


# ==================================================================================================#
# MAIN DEMO FUNCTION                                                                               #
# ==================================================================================================#

def dynamic_xpath_demo(driver):
    """
    Runs the full Dynamic XPath demonstration:
      - Opens the GUVI homepage
      - Runs Task 3 (Relative XPath) for every navbar element
      - Runs Task 4 (Axes XPath) for every navbar element
      - Closes the browser in the finally block
    """
    try:

        # Go to the URL - https://www.guvi.in/
        print("Loading GUVI Home Page")
        driver.get(GUVI_BASE_URL)
        time.sleep(1)

        # -- Locate the first element: 'LIVE Classes' navbar link -----------------
        # This is the first element in the navbar in GUVI homepage
        print(f" FIRST ELEMENT in Navigation Bar - '{NAV_BAR_LINK_TEXT_LIST[0]}'")
        element = generate_rel_xpath_and_find_element(driver, NAV_BAR_LINK_TEXT_LIST[0], "self")
        print_element(element, NAV_BAR_LINK_TEXT_LIST[0], "self")

        # Relative XPATH Demonstration
        print("\n+-----------------------------------------------+")
        print("+        RELATIVE XPATH DEMONSTRATIONS          +")
        print("+-----------------------------------------------+")

        for navbar_el_name in NAV_BAR_LINK_TEXT_LIST:
            print(f"\nNavigation bar element: '{navbar_el_name}'")
            print("========================================")

            # -- 3a. Find the PARENT element -------------------
            # parent:: -> moves one level up in the DOM tree
            parent_element = generate_rel_xpath_and_find_element(driver, navbar_el_name, "parent")
            print_element(parent_element, navbar_el_name, "parent")

            # -- 3b. Find the FIRST CHILD element -------------------
            # child::*[1]     -> selects the first child element of any type
            firstchild_element = generate_rel_xpath_and_find_element(driver, navbar_el_name, "first child")
            print_element(firstchild_element, navbar_el_name, "first child")

            # -- 3c. Locate the second sibling element (If any) -------------------
            # following-sibling::*[2] -> the second sibling that comes AFTER current element
            secondsibling_element = generate_rel_xpath_and_find_element(driver, navbar_el_name, "second sibling")
            print_element(secondsibling_element, navbar_el_name, "second sibling")

            # -- 3d. Select PARENT of the element that has attribute 'href' -------------------
            # This finds the parent of the first <a> tag that has an href attribute
            print(f" ELEMENT with href - '{navbar_el_name!r}'")
            element = generate_rel_xpath_and_find_element(driver, navbar_el_name, "self with href", href=True)
            print_element(element, NAV_BAR_LINK_TEXT_LIST[0], "self with href")

            print(f" PARENT of element with href - '{navbar_el_name!r}'")
            parent_of_element_with_href = generate_rel_xpath_and_find_element(driver, navbar_el_name, "parent",
                                                                              href=True)
            print_element(parent_of_element_with_href, navbar_el_name, "parent")

        # AXES XPATH Demonstration
        print("\n+-----------------------------------------------+")
        print("+            AXES XPATH DEMONSTRATIONS          +")
        print("+-----------------------------------------------+")

        for navbar_el_name in NAV_BAR_LINK_TEXT_LIST:
            # -- 4a. Find ALL ANCESTOR elements  -------------------
            # ancestor::* → every element that contains 'element' up to <html>
            ancestor_elements = generate_rel_xpath_and_find_element(driver, navbar_el_name, "all ancestor elements")
            print_elements(ancestor_elements, navbar_el_name, "all ancestor elements")

            # -- 4b. Locate ALL FOLLOWING SIBLINGS -------------------
            # following-sibling::* → every sibling element AFTER 'element'
            following_sibling_elements = generate_rel_xpath_and_find_element(driver, navbar_el_name,
                                                                             "all following siblings")
            print_elements(following_sibling_elements, navbar_el_name, "all following siblings")

            # -- 4c. Select ALL PRECEDING elements -------------------
            # preceding::* → every element that appears BEFORE 'element'
            preceding_elements = generate_rel_xpath_and_find_element(driver, navbar_el_name, "all preceding elements")
            print_elements(preceding_elements, navbar_el_name, "all preceding elements")

    finally:
        # Close browser
        print("TEARDOWN: Closing GUVI Home Page browser")
        driver.quit()


def main():
    """
    Entry point: launches Chrome, maximizes the window,
    runs the dynamic XPath demo, and exits.
    """
    # Launch browser
    print("Launching Chrome browser...")
    driver = webdriver.Chrome()

    # Maximize browser
    driver.maximize_window()

    dynamic_xpath_demo(driver)


if __name__ == "__main__":
    main()
