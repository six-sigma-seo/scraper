import scrapy
import datetime


class Item(scrapy.Spider):
    name = "seo"

    def __init__(self, domain='', *args, **kwargs):
        super(Item, self).__init__(*args, **kwargs)
        self.start_urls = [domain]

    custom_settings = {
        'FEED_URI': 'seo.json',
        'FEED_FORMAT': 'json',
        'CONCURRENT_REQUESTS': 24,
        'MEMUSAGE_LIMIT_MB': 2048,
        'MEMUSAGE_NOTIFY_MAIL': ['csgalindos@hotmail.com'],
        'ROBOTSTXT_OBEY': True,
        'USER_AGENT': 'seomaster',
        'FEED_EXPORT_ENCODING': 'utf-8'
    }

    def parse(self, response):
        # date information
        today = datetime.date.today().strftime('%d-%m-%Y')

        # Language Tag
        language_tag = response.xpath('/html/@lang').get()
        if language_tag:
            booleanlanguage_tag = True
        else:
            booleanlanguage_tag = False

        # Title
        # get title tag
        titlepage = response.xpath('//title/text()').get()
        # get number of titles tag in page
        numbertitlepage = len(response.xpath('//title/text()').getall())

        # tag Title duplicated
        if numbertitlepage == 1:
            title_duplicated = False
        else:
            title_duplicated = True

        # check if exist some information in title tag
        if titlepage == None:
            sizetitlepage = False
        else:
            sizetitlepage = len(titlepage)

        # check dimension of text in title tag
        if sizetitlepage == 0:
            rigthdimentiontitlepage = 'untitle'
        elif sizetitlepage <= 60 and sizetitlepage >= 50:
            rigthdimentiontitlepage = True
        elif sizetitlepage > 60:
            rigthdimentiontitlepage = False
        elif sizetitlepage == False:
            rigthdimentiontitlepage = False
        else:
            rigthdimentiontitlepage = False

        # check dimension of text in title tag
        if numbertitlepage >= 0:
            booleannumbertitlepage = False
        elif numbertitlepage < 2:
            booleannumbertitlepage = False
        else:
            booleannumbertitlepage = True

        # Meta Description
        # meta description information
        meta_description = response.xpath(
            '//meta[@name="description"]/@content').get()

        # check number of meta description tags
        numbermeta_description = len(response.xpath(
            '//meta[@name="description"]/@content').getall())

        # dimension of meta description tag
        sizemetadescription = len(meta_description)

        # check of dimension about meta description tag
        if sizemetadescription == 0:
            rigthdimentionmetadescription = 'undescription'
        elif sizemetadescription <= 155:
            rigthdimentionmetadescription = True
        else:
            rigthdimentionmetadescription = False

        # Meta Keyword
        # meta Keyword information
        meta_keywords = response.xpath(
            '//meta[contains(@name,"keywords")]').getall()

        # check number of meta keyword tags
        numbermeta_keywords = len(response.xpath(
            '//meta[contains(@name,"keywords")]').getall())

        # H tags
        # get information of H1 tag
        htitle = response.xpath('//h1/text()').get()
        # number of H1 tag have
        numberhtitle = len(response.xpath('//h1/text()').getall())
        # Tags H1 y H2 Counter
        number_tags_h1 = len(response.xpath('//h1/text()').getall())
        number_tags_h2 = len(response.xpath('//h2/text()').getall())

        # review if exist some
        if numberhtitle == 1:
            boolean_numberhtitle = True
        else:
            boolean_numberhtitle = False

        # img
        # get img without alt atribute
        imgwithoutalt = response.xpath('//img[not(@alt)]').getall()
        # total elements the img of the page
        totalimg = len(response.xpath('//img').getall())
        # number of img without alt atribute
        numberimgwithoutalt = len(response.xpath('//img[not(@alt)]').getall())
        # img with attribute alt empty
        imgwithaltempty = response.xpath('//img[@alt=""]/@src').getall()
        # return tha number of img empty
        numberimgwithaltempty = len(response.xpath('//img[@alt=""]').getall())
        # show the percentage of img with something with alt empty
        percentajeemptyaltinimg = int((numberimgwithaltempty/totalimg)*100)
        # check number of img rith
        if len(imgwithoutalt) >= 0:
            booleanimgwithoutalt = False
        else:
            booleanimgwithoutalt = True

        # old tags
        # check if the page use some old tags
        old_tags = []
        list_old_tags = ['applet', 'acronym', 'bgsound', 'dir', 'frame', 'frameset', 'noframes', 'hgroup', 'isindex', 'listing', 'xmp',
                         'noembed', 'strike', 'basefont', 'big', 'blink', 'center', 'font', 'marquee', 'multicol', 'nobr', 'spacer''tt', 'menu']
        for tag in list_old_tags:
            found_tags = response.xpath(f'//{tag}').getall()
            if len(found_tags) > 0:
                old_tags.append(found_tags)

        # retur a boolena information if use someone old tags
        if old_tags:
            boolean_old_tags = False
        else:
            boolean_old_tags = True

        # Aria - label
        # tag Button without Arial-labels
        buttons = response.xpath('//button').getall()
        buttons_wo_aria = response.xpath('//button[not(@aria-label)]').getall()
        inputs = response.xpath('//input').getall()
        inputs_wo_aria = response.xpath('//input[not(@aria-label)]').getall()

        # review about if buttons and inputs have the aria label
        if ((buttons_wo_aria == buttons) and (inputs_wo_aria == inputs)):
            boolean_aria = True
        else:
            boolean_aria = False

        # Semanthic Structure
        # Header is True?
        header = False
        header_found = response.xpath('//header').getall()
        if len(header_found) == 1:
            header = True

        # Body is True?
        main = False
        main_found = response.xpath('//main').getall()
        if len(main_found) == 1:
            main = True

        # Body is section?
        section = False
        section_found = response.xpath('//section').getall()
        if len(section_found) == 1:
            section = True

        # Footer is True?
        footer = False
        footer_found = response.xpath('//footer').getall()
        if len(footer_found) == 1:
            footer = True

        # validate if some tags like header, main, footer or section exits in the web page
        if ((footer == True) and (header == True) and (main == True) and (section == True)):
            boolean_structure_semantic = True
        else:
            boolean_structure_semantic = False

        # social meta tags
        # review the information of set in faceboo, facebook and twitter
        meta_google = response.xpath(
            '//meta[contains(@property,"og")]').getall()
        meta_facebook = response.xpath(
            '//meta[contains(@property,"fb")]').getall()
        meta_twitter = response.xpath(
            '//meta[contains(@name,"twitter")]').getall()

        # review if exist information of social media tags
        if (meta_twitter and meta_facebook and meta_google):
            boolean_meta_sm = True
        else:
            boolean_meta_sm = False

        yield {
            'date': today,
            'titlepage': titlepage,
            'metadescription': meta_description,

            'booleanAT': booleanimgwithoutalt,
            'booleanTP': booleannumbertitlepage,
            'booleanDI': booleanlanguage_tag,
            'booleanES': boolean_structure_semantic,
            'booleanEA': boolean_aria,
            'booleanJT': boolean_numberhtitle,
            'booleanED': boolean_old_tags,
            'booleanMI':  boolean_meta_sm,

            'imgwithoutalt': imgwithoutalt,
            'qtyimgwithoutalt': numberimgwithoutalt,
            'imgwithaltempty': imgwithaltempty,
            'qtyimgwithaltempty': numberimgwithaltempty,
            'totalimg': totalimg,
            'percentajeemptyaltinimg': percentajeemptyaltinimg,

            'metadescription': meta_description,
            'lenthmetadescription': sizemetadescription,
            'rigthdimensionmetadescription': rigthdimentionmetadescription,
            'qtymetadescription': numbermeta_description,
            'google': meta_google,
            'facebook': meta_facebook,
            'twitter': meta_twitter,

            'titlepage': titlepage,
            'qtytitlepage': numbertitlepage,
            'lenthtitlepage': sizetitlepage,
            'rigthdimensiontitlepage': rigthdimentiontitlepage,

            'h1title': htitle,
            'qtyh1title': numberhtitle,

            'keywords': meta_keywords,
            'qtymeta_keywords': numbermeta_keywords,

            'title_duplicated': title_duplicated,
            'old_tags': old_tags,
            'buttons_without_arial_tags': buttons,
            'number_tags_h1': number_tags_h1,
            'number_tags_h2': number_tags_h2,
            'language_tag': language_tag,
            'header': header,
            'footer': footer
        }
