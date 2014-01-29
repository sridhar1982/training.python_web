#import amazonproduct
import pprint
import requests
import json
from lxml import etree
from lxml import html
from StringIO import StringIO

class EbayLookup(object):

    apikey='Mycompan-7f38-4f11-a008-67694d08f7b1'

    def __init__(self):
         self.api_url='http://svcs.ebay.com/services/search/FindingService/v1'

    def  makerequest(self,params):
        self.resp = requests.get(self.api_url, params=parameters)
        self.resp.raise_for_status()
    
    def parse_resp(self):
        data = json.loads(self.resp.text)
        for items in data['findItemsByKeywordsResponse'][0]['searchResult'][0]['item'][0:10]:
            print items['title'][0].encode('ascii','ignore')
            print items['sellingStatus'][0]['currentPrice'][0]['__value__']
            print items['viewItemURL'][0].encode('ascii','ignore')

parameters = {
            'OPERATION-NAME':'findItemsByKeywords',
            'SERVICE-VERSION':'1.0.0',
            'SECURITY-APPNAME':EbayLookup.apikey,
            'RESPONSE-DATA-FORMAT':'json',
            'keywords':'macbook pro 13 retina',
            'itemFilter(0).name':'Condition',
            'itemFilter(0).value':'New',
            'itemFilter(1).name':'MaxPrice',
            'itemFilter(1).value':'1500.00',
            #'itemFilter(2).name':'TopRatedSellerOnly',
            #'itemFilter(2).value':'true'
            #'itemFilter(3).name':'ReturnsAcceptedOnly',
            #'itemFilter(3).value':'true'
            #'itemFilter(4).name':'ExpeditedShippingType',
            #'itemFilter(4).value':'Expedited'
            #'itemFilter(5).name':'MaxHandlingTime',
            #'itemFilter(5).value':'1'
            #'itemFilter(6).name':'Currency',
            #'itemFilter(6).value':'USD'
        }


class AmazonLookup(object):

    config = {
    'access_key': 'AKIAIKB4DUV5OXRK2FZQ',
    'secret_key': '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',
    'associate_tag': 'wwwmywebpageat-20',
    'locale': 'us'
     }

    def __init__(self):
        try:
            import amazonproduct
        except ImportError :
            print "Needs amazonproduct api for this code to work"
            sys.exit(0)
        self.api = amazonproduct.API(cfg=self.config)

    def itemsearch(self,*args,**params):
        items = self.api.item_search(*args, **params)
        self.listASIN=[(item.ItemAttributes.Title,item.ASIN) for item in items]
        
    def itemlookup(self):
        for asin in self.listASIN[0:3]:
            node=self.api.item_lookup(str(asin[1]),ResponseGroup="Offers",Condition='All')
            for a in node.Items.Item.Offers.Offer:
                yield (a.OfferListing.Price.FormattedPrice, a.OfferAttributes.Condition,str(asin[0]))


    def getreviews(self):
            return self.__reviewsUrl(str(self.listASIN[0][1]))


    def __reviewsUrl(self,ASIN):
        result = self.api.item_lookup(ASIN, ResponseGroup='Reviews',
                    TruncateReviewsAt=256, IncludeReviewsSummary=False,Sort='reviewrank')
        iframeurl=result.xpath('//*[local-name()="IFrameURL"]/text()')[0].strip()
        reviews=requests.get(iframeurl)
        parser = etree.HTMLParser()
        tree   = etree.parse(StringIO(reviews.text), parser)
        #result = etree.tostring(tree.getroot(),pretty_print=True, method="html")
        reviewlink= tree.xpath('//a[contains(text(), "customer reviews...")]/@href')[0]
        self.reviewnode = html.parse(reviewlink)
        for reviews in self.reviewnode.xpath('//div[@class="reviewText"]/text()'):
            yield reviews


    def getNextPageReviews(self):
        #not functional full
        next=self.reviewnode.xpath('//a[contains(text(), Next)]/@href')[0]
        return next


if __name__=='__main__':


    #do ebay search
    print "%s\n %s\n %s" %('*'*82,"prices for new macbook pro 13 retina from eBay",'*'*82)
    ebay = EbayLookup()
    ebay.makerequest(parameters)
    ebay.parse_resp()

    print "%s\n %s\n %s" %('*'*82,"prices for new macbook pro 13 retina from Amazon",'*'*82)


    #amazon search
    amazonsearch=AmazonLookup()
    params={'Condition':'New','Keywords':'Macbook pro 13 retina','MinimumPrice':600,'limit':5}
    amazonsearch.itemsearch('Electronics',**params)
    for i in amazonsearch.itemlookup():
        print i

    print '*'*40 + 'customer reviews'+'*'*40

    count=1
    for reviews in amazonsearch.getreviews():
        print "Review:  %s %s\n %s" %(count,reviews,'-'*100)
        count+=1


