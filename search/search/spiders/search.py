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
        today = datetime.date.today().strftime('%d-%m-%Y')
        titlepage = response.xpath('//title/text()').get()
        sizetitlepage = len(titlepage)
        if sizetitlepage == 0:
            rigthdimentiontitlepage = 'untitle'
        elif sizetitlepage <= 60 and sizetitlepage >= 50:
            rigthdimentiontitlepage = True
        elif sizetitlepage > 60:
            rigthdimentiontitlepage = False
        else:
            rigthdimentiontitlepage = False
        numbertitlepage = len(response.xpath('//title/text()').getall())

        meta_description = response.xpath(
            '//meta[@name="description"]/@content').get()
        sizemetadescription = len(meta_description)
        if sizemetadescription == 0:
            rigthdimentionmetadescription = 'undescription'
        elif sizemetadescription <= 155:
            rigthdimentionmetadescription = True
        else:
            rigthdimentionmetadescription = False
        numbermeta_description = len(response.xpath(
            '//meta[@name="description"]/@content').getall())

        meta_keywords = response.xpath(
            '//meta[contains(@name,"keywords")]').getall()
        numbermeta_keywords = len(response.xpath(
            '//meta[contains(@name,"keywords")]').getall())

        htitle = response.xpath('//h1/text()').get()
        numberhtitle = len(response.xpath('//h1/text()').getall())

        imgwithoutalt = response.xpath('//img[not(@alt)]').getall()
        numberimgwithoutalt = len(response.xpath('//img[not(@alt)]').getall())

        imgwithaltempty = response.xpath('//img[@alt=""]/@src').getall()
        numberimgwithaltempty = len(response.xpath('//img[@alt=""]').getall())

        totalimg = len(response.xpath('//img').getall())
        percentajeemptyaltinimg = int((numberimgwithaltempty/totalimg)*100)

        meta_google = response.xpath(
            '//meta[contains(@property,"og")]').getall()
        meta_facebook = response.xpath(
            '//meta[contains(@property,"fb")]').getall()
        meta_twitter = response.xpath(
            '//meta[contains(@name,"twitter")]').getall()

        # New Features

        # Tag Title duplicated
        titles_page = response.xpath('//title/text()').getall()
        if len(titles_page) == 1:
            title_duplicated = False
        else:
            title_duplicated = True

        # Old tags
        old_tags = []
        list_old_tags = ['applet', 'acronym', 'bgsound', 'dir', 'frame', 'frameset', 'noframes',
                         'hgroup', 'isindex', 'listing', 'xmp', 'noembed', 'strike', 'basefont',
                         'big', 'blink', 'center', 'font', 'marquee', 'multicol', 'nobr', 'spacer'
                         'tt', 'menu']
        for tag in list_old_tags:
            found_tags = response.xpath(f'//{tag}').getall()
            if len(found_tags) > 0:
                old_tags.append(found_tags)


        # Tag Button without Arial-labels
        buttons_without_arial_tags = False
        buttons = response.xpath('//button[not(aria-label)]').getall()

        # Tags H1 y H2 Counter
        number_tags_h1 = len(response.xpath('//h1/text()').getall())
        number_tags_h2 = len(response.xpath('//h2/text()').getall())

        # Language Tag
        language_tag = response.xpath('/html/@lang').get()

        # Semanthic Structure
        # Header is True?
        header = False
        header_found = response.xpath('//head').getall()
        if len(header_found) == 1:
            header = True


        # Body is True?
        body = False
        body_found = response.xpath('//body')
        if len(body_found) == 1:
            body = True

        # Footer is True?
        footer = False
        footer_found = response.xpath('//footer')
        if len(footer_found) == 1:
            footer = True
        
        yield {
            'date': today,
            'titlepage': titlepage,
            'qtytitlepage': numbertitlepage,
            'lenthtitlepage': sizetitlepage,
            'rigthdimensiontitlepage': rigthdimentiontitlepage,
            'metadescription': meta_description,
            'lenthmetadescription': sizemetadescription,
            'rigthdimensionmetadescription': rigthdimentionmetadescription,
            'qtymetadescription': numbermeta_description,
            'keywords': meta_keywords,
            'qtymeta_keywords': numbermeta_keywords,
            'h1title': htitle,
            'qtyh1title': numberhtitle,
            'imgwithoutalt': imgwithoutalt,
            'qtyimgwithoutalt': numberimgwithoutalt,
            'imgwithaltempty': imgwithaltempty,
            'qtyimgwithaltempty': numberimgwithaltempty,
            'totalimg': totalimg,
            'percentajeemptyaltinimg': percentajeemptyaltinimg,
            'google': meta_google,
            'facebook': meta_facebook,
            'twitter': meta_twitter,
            'title_duplicated': title_duplicated,
            'old_tags': old_tags,
            'buttons_without_arial_tags': buttons,
            'number_tags_h1': number_tags_h1,
            'number_tags_h2': number_tags_h2,
            'language_tag': language_tag,
            'header': header,
            'body': body,
            'footer': footer
        }
