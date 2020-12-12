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
        if titlepage == None:
            sizetitlepage = False
        else:
            sizetitlepage = len(titlepage)

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
        numbertitlepage = len(response.xpath('//title/text()').getall())

        if numbertitlepage >= 0:
            booleannumbertitlepage = False
        elif numbertitlepage < 2:
            booleannumbertitlepage = False
        else:
            booleannumbertitlepage = True

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
        if numberhtitle <= 1:
            boolean_numberhtitle = False
        else:
            boolean_numberhtitle = True

        imgwithoutalt = response.xpath('//img[not(@alt)]').getall()

        if len(imgwithoutalt) >= 0:
            booleanimgwithoutalt = False
        else:
            booleanimgwithoutalt = True

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

        if (meta_twitter and meta_facebook and meta_google):
            boolean_meta_sm = True
        else:
            boolean_meta_sm = False

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

        if old_tags:
            boolean_old_tags = False
        else:
            boolean_old_tags = True

        # Tag Button without Arial-labels
        buttons = response.xpath('//button').getall()
        buttons_wo_aria = response.xpath('//button[not(@aria-label)]').getall()
        inputs = response.xpath('//input').getall()
        inputs_wo_aria = response.xpath('//input[not(@aria-label)]').getall()

        # count_buttons = response.xpath('//button/@aria-label').getall()
        # for i in count_buttons:
        #     if len(i) <= 6:
        #         dimension_buttons = True,
        #     else:
        #         dimension_buttons = False

        # count_inputs = response.xpath('//input/@aria-label').getall()
        # for i in count_inputs:
        #     if len(i) <= 6:
        #         dimension_inputs = True,
        #     else:
        #         dimension_inputs = False

        if ((buttons_wo_aria == buttons) and (inputs_wo_aria == inputs)):
            boolean_aria = True
        else:
            boolean_aria = False

            # Tags H1 y H2 Counter
        number_tags_h1 = len(response.xpath('//h1/text()').getall())
        number_tags_h2 = len(response.xpath('//h2/text()').getall())

        # Language Tag
        language_tag = response.xpath('/html/@lang').get()
        if language_tag:
            booleanlanguage_tag = True
        else:
            booleanlanguage_tag = False

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

        if ((footer == True) and (header == True) and (main == True) and (section == True)):
            boolean_structure_semantic = True
        else:
            boolean_structure_semantic = False

        yield {
            'date': today,
            'titlepage': titlepage,
            'metadescription': meta_description,

            'titleAT': "Alternativas Textuales",
            'descriptionAT': "Todos los elementos no visuales de la pagina deben incluir la etiqueta alt para facilitar la lectura por el robot de Google.",
            'booleanAT': booleanimgwithoutalt,
            'endpointAT': "/textualalternatives",

            'titleTP': "Titulo de Pagina",
            'descriptionTP': "Unicamente debe exister una etiqueta title dentro de la estructura de la pagina y el contendo de esta debe ser descriptivo en relación al contenido de la pagina.",
            'booleanTP': booleannumbertitlepage,
            'endpointTP': "/titlepage",

            'titleDI': "Declaración de Idioma",
            'descriptionDI': "Se debe especificar el idioma de la pagina con la etiqueta: <html lang=eng>.",
            'booleanDI': booleanlanguage_tag,
            'endpointDI': "ee",

            'titleES': "Estructura Semantica",
            'descriptionES': "La pagina deberia utilizar un mínimo de etiquetas semánticas las cuales son: header, section, footer, main.",
            'booleanES': boolean_structure_semantic,
            'endpointES': "el endpoint a consular para este feature",

            'titleEA': "Etiqueta Arial-label",
            'descriptionEA': "Las etiquetas de button e input deberian tener el atributo aria-label y el contenido de este debe ser superior a 6 caracteres.",
            'booleanEA': boolean_aria,
            'endpointEA': "el endpoint a consular para este feature",

            'titleJT': "Jerarquias Textuales",
            'descriptionJT': "La etiquetas de titulos deben seguir un jerarquia de acuerdo a su orden, solo deberia usarse una vez la etiqueta <h1> por ejemplo.",
            'booleanJT': boolean_numberhtitle,
            'endpointJT': "/textualhierarchies",

            'titleED': "Etiquetas en Desuso",
            'descriptionED': "Con el paso de las versiones de html se han dejado de usar ciertas etiquetas, se recomienda su sustitución.",
            'booleanED': boolean_old_tags,
            'endpointED': "/disusedlabels",

            'titleMI': "Meta Información",
            'descriptionMI': "Se recomienda el uso de las etiquetas de meta información para asegurar que el robot de google entienda nuestra pagina. Así como para la correcta representación en redes sociales.",
            'booleanMI':  boolean_meta_sm,
            'endpointMI': "/metadescription",

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

            'qtytitlepage': numbertitlepage,
            'lenthtitlepage': sizetitlepage,
            'rigthdimensiontitlepage': rigthdimentiontitlepage,

            'keywords': meta_keywords,
            'qtymeta_keywords': numbermeta_keywords,
            'h1title': htitle,
            'qtyh1title': numberhtitle,





            'title_duplicated': title_duplicated,
            'old_tags': old_tags,
            'buttons_without_arial_tags': buttons,
            'number_tags_h1': number_tags_h1,
            'number_tags_h2': number_tags_h2,
            'language_tag': language_tag,
            'header': header,
            # 'body': body,
            'footer': footer
        }
