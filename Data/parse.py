from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                print('error')
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)


def get_data(url):
    f = open('strains.csv', 'a')
    raw_html = simple_get(url)

    soup = BeautifulSoup(raw_html, 'html.parser')

    name = ''
    try:
        name = " ".join(soup.title.getText().split(" ")[:-5])
    except:
        print('error in getting name')
  #  print(name)

    desc_text = ''
    try:
        desc = soup.find('div', class_='description')
        desc_text = desc.p.getText()
  #      print(desc.p.getText())
    except:
        print('',end='')

   # print()
   # print('GROW INFO:')

    grow_info_str = ''
    try:
        grow_info = soup.find_all('div', class_=['growInfoRow','growInfoRow desktopYield'])
        for grow in grow_info:
            val = grow.find(lambda tag: tag.name == 'div' and 
                                tag.get('class') and tag.get('class') == ['selected'] )
            label = grow.find(lambda tag: tag.name == 'div' and
                                tag.get('class') and tag.get('class') == ['strain__data'])
            label = label.text.strip()
            val = val.text.strip()

        #    print(label + ':' + val)
            grow_info_str += label + ':' + val + ','
      #  print()
    except:
        print('',end='')
                        

    effects = ''
    medical = ''
    negatives = ''

    try:
        categories = soup.find_all(lambda tag: tag.name == 'div' and
                                    tag.get('class') == ['m-histogram'])
        

        for cat in categories:
            category = cat['ng-show'].split('===')[1][1:-1]
          #  print(category)

            hists = cat.find_all(lambda tag: tag.name == 'div' and 
                                            tag.get('class') == ['m-histogram-item-wrapper'])
            for item in hists:
                label = item.find('div', class_='m-attr-label copy--sm').string
                val = item.find('div', class_='m-attr-bar')['style'].split(':')[1][:-1]
                val = round(float(val),2)
                if category == 'Effects':
                    effects += label + ':' + str(val) + ','
                elif category == 'Medical':
                    medical += label + ':' + str(val) + ','
                elif category == 'Negatives':
                    negatives += label + ':' + str(val) + ','
         #       print(label + ':sdf ' + str(val))
         #   print()

            
            
    except:
        print('',end='')

    all_flavors = 'Ammonia Apple Apricot Berry Blue Cheese Blueberry Butter Cheese Chemical Chestnut Citrus Coffee Diesel Earthy Flowery Grape Grapefruit Honey Lavender Lemon Lime Mango Menthol Mint Nutty Orange Peach Pear Pepper Pine Pineapple Plum Pungent Rose Sage Skunk Spicy/Herbal Strawberry Sweet Tar Tea Tobacco Tree Fruit Tropical Vanilla Violet Woody'
    
    flavor_str = ''
    try:
        flavors = soup.find_all(lambda tag: tag.name == 'li' and
                                    tag.get('class') and 
                                        tag.get('class')[0].find("grid-1-3 grid-xs-1-3 copy--centered colored-background") and
                                            tag.get('title') and tag.get('title').find(all_flavors))
      #  print('FLAVORS:')
        if flavors:
            for flavor in flavors:
            #    print(flavor['title'])
                flavor_str += flavor['title'] + ','
     #   print()
    except:
        print('',end='')
   # print('PARENTS:')

    parents_str = ''
    try:
        lineage = soup.find('div', class_='strain__lineage strain__dataTab')
        if lineage:
            parent = lineage.find_all(lambda tag: tag.name == 'a' and tag.get('href'))
            if parent:
                for p in parent:
                    par = p['href'].split('/')
                #    print('type: ' + par[len(par) - 2] + ' strain: ' + par[len(par) - 1])
                    parents_str += par[len(par) - 2] + ':' + par[len(par) - 1] + ','
    except:
        print('',end='')

    rate_str = ''
    try:
        rate = soup.find(lambda tag: tag.name == 'div' and 
                            tag.get('itemprop') and tag.get('itemprop') == 'aggregateRating')
        avg_rating = rate.find(lambda tag: tag.name == 'span' and tag.get('star-rating'))
        rate_str = avg_rating['star-rating']
    except:
        print('',end='')
    
    num_rate = ''
    try:
        num_ratings = rate.find(lambda tag: tag.name == 'span' and tag.get('itemprop') and
                            tag.get('itemprop') == 'reviewCount')
        num_rate = num_ratings.text
    except:
        print('',end='')
  #  print()

    
  #  if avg_rating and avg_rating['star-rating']:
    #    print(avg_rating['star-rating'])
   # if num_ratings and num_ratings.text:
     #   print(num_ratings.text)

    f.write(name + ';' + desc_text + ';' + grow_info_str 
            + ';' + effects + ';' + medical + ';' + negatives + ';' + \
             flavor_str+ ';' + parents_str + ';' + rate_str + ';' + num_rate+'\n')