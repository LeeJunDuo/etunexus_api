# -*- coding: utf-8 -*-

from baseapp import BaseApp
from enum import *
from emc import Group, DataSource


class BandGene(dict):
    """ Structure for a gene-based band

    Fields:
        geneId (str): The gene id
        cid (int): The data source id to calculate the band
        operator (str): The band operator to calculate the band
        operand (str): The operands to calculate the band
    """

    def __init__(self, gene_id, cid, operator, operand):
        assert gene_id and cid and operator and operand
        super(BandGene, self).__init__({
            'geneId': gene_id,
            'cid': cid['id'] if isinstance(cid, DataSource) else cid,
            'operator': operator,
            'operand': operand
        })

    @classmethod
    def from_dict(cls, dict_obj):
        assert dict_obj
        return cls(dict_obj['geneId'], dict_obj['cid'], dict_obj['operator'], dict_obj['operand'])


class BandCombine(dict):
    """ Structure for a combined band

    Fields:
        bandIds (list): List of band ids to combine
        operators (list): List of operators using to combine the bands (only the first element is used yet)
    """

    def __init__(self, bands, operators):
        assert bands and operators
        super(BandCombine, self).__init__({
            'bandIds': [x['id'] if isinstance(x, Band) else x for x in bands],
            'operators': operators
        })

    @classmethod
    def from_dict(cls, dict_obj):
        assert dict_obj
        return cls(dict_obj['bandIds'], dict_obj['operators'])


class Band(dict):
    """ Structure for a band
    
    Fields:
        categoryId (int): The band category of the band belongs to
        name (str): Band name
        description (str): Band description
        type (str): Band type, refer to 'BandType' for valid values
        targetGene (obj): Gene setting if type=gene or type=fixedgene
        targetBand (obj): Combine bands if type=combine

        needRefresh (bool): Need to refresh the band or not
        snapshotInfo (obj): Snapshot info (if a snap-shot band), or None for pure band

        id (int): The auto id
        amount (int): Amount of users in the band
        updateTime (long): The band update time in Epoch (milliseconds)
    """

    def __init__(self, category, name, description,
                 type, target_gene=None, target_band=None,
                 need_refresh=True, snapshot_info=None,
                 id=None, amount=None, update_time=None):
        super(Band, self).__init__({
            'categoryId': category['id'] if isinstance(category, BandCategory) else category,
            'name': name,
            'description': description,
            'needRefresh': need_refresh,
            'type': type,
            'targetGene': target_gene,
            'targetBand': target_band,
            'snapshotInfo': snapshot_info,
            'id': id,
            'amount': amount,
            'updateTime': update_time
        })

    @classmethod
    def from_dict(cls, dict_obj):
        assert dict_obj
        return cls(dict_obj['categoryId'], dict_obj['name'], dict_obj['description'],
                   dict_obj['type'], dict_obj.get('targetGene'), dict_obj.get('targetBand'),
                   dict_obj['needRefresh'], dict_obj.get('snapshotInfo'),
                   dict_obj.get('id'), dict_obj.get('amount'), dict_obj.get('updateTime'))

    @classmethod
    def from_dict_with_ext_cat_id(cls, dict_obj, category_id):
        assert dict_obj and category_id
        return cls(category_id, dict_obj['name'], dict_obj['description'],
                   dict_obj['type'], dict_obj.get('targetGene'), dict_obj.get('targetBand'),
                   dict_obj['needRefresh'], dict_obj.get('snapshotInfo'),
                   dict_obj.get('id'), dict_obj.get('amount'), dict_obj.get('updateTime'))


class GeneUIInfo(dict):
    """ Structure for gene UI info

    Fields:
        Xaxis_id (str): The string id of gene chart x-axis
        Yaxis_id (str): The string id of gene chart y-axis
        unit (str): The string id of gene unit (used on gene filter UI, etc.)
        Xaxis (str): The (localized) string of gene chart x-axis directly set by system operator
        Xaxis (str): The (localized) string of gene chart y-axis directly set by system operator
    """

    def __init__(self, x_axis_id=None, y_axis_id=None, unit=None, x_axis=None, y_axis=None):
        super(GeneUIInfo, self).__init__({
            'Xaxis_id': x_axis_id,
            'Yaxis_id': y_axis_id,
            'unit': unit,
            'Xaxis': x_axis,
            'Yaxis': y_axis
        })

    @classmethod
    def from_dict(cls, dict_obj):
        assert dict_obj
        return cls(dict_obj.get('Xaxis_id'), dict_obj.get('Yaxis_id'), dict_obj.get('unit'),
                   dict_obj.get('Xaxis'), dict_obj.get('Yaxis'))


class FixedGene(dict):
    """ Structure for fixed (external) gene

    Fields:
        id (str): The id of the fixed gene. It should be unique in a fixed subcategory
        name (str); Gene name
        timerange (int): Gene time range
        type (str): Gene type, refer to GeneType for valid values
        chartType (str): Gene chart type, refer to GeneChartType for valid values
        uiInfo (obj): Gene UI info
    """

    def __init__(self, id, name, time_range, type, chart_type, ui_info):
        assert id and name and time_range is not None and type and chart_type and ui_info
        super(FixedGene, self).__init__({
            'id': id,
            'name': name,
            'timerange': time_range,
            'type': type,
            'chartType': chart_type,
            'uiInfo': ui_info if isinstance(ui_info, GeneUIInfo) else GeneUIInfo.from_dict(ui_info)
        })

    @classmethod
    def from_dict(cls, dict_obj):
        assert dict_obj
        return cls(dict_obj['id'], dict_obj['name'], dict_obj['timerange'], dict_obj['type'], dict_obj['chartType'],
                   dict_obj['uiInfo'])


class FixedGeneCategory(dict):
    """ Structure for fixed (external) gene categories

    Fields:
        name (str): Fixed gene name
        subcategories (list): A list of FixedGeneCategory as subcategories
        genes (list): A list of

        id (int): The auto id
    """

    def __init__(self, name, subcategories, genes, id=None):
        assert name and subcategories is not None and isinstance(subcategories, list) and genes is not None and isinstance(genes, list)
        super(FixedGeneCategory, self).__init__({
            'name': name,
            'subcategories': [x if isinstance(x, FixedGeneCategory) else FixedGeneCategory.from_dict(x) for x in subcategories],
            'genes': [x if isinstance(x, FixedGene) else FixedGene.from_dict(x) for x in genes],
            'id': id
        })

    @classmethod
    def from_dict(cls, dict_obj):
        assert dict_obj
        return cls(dict_obj['name'], dict_obj['subcategories'], dict_obj['genes'], dict_obj.get('id'))


class BandCategory(dict):
    """ Structure for a band category

    Fields:
        name (str): The band category name
        bands (list): A list of Bands
        id (int): The auto id
    """

    def __init__(self, name, bands=None, id=None):
        assert name
        if bands is None:
            bands = []
        assert isinstance(bands, list)
        super(BandCategory, self).__init__({
            'name': name,
            'bands': [x if isinstance(x, Band) else Band.from_dict_with_ext_cat_id(x, id) for x in bands],
            'id': id
        })

    def to_simple(self):
        return {'name': self['name']}

    @classmethod
    def from_dict(cls, dict_obj):
        return cls(dict_obj['name'], dict_obj.get('bands'), dict_obj.get('id'))


class EI3(BaseApp):
    """ Encapsulate Etu Insight (v3) API """

    __APP_NAME = 'EI3'
    __HOST = 'eihome.online.etunexus.com'
    __API_BASE = '/EI/V3/service/v1'
    __SHIRO_CAS_BASE = '/EI/V3/shiro-cas'

    def __init__(self, cas, host=None, api_base=None, shiro_cas_base=None):
        """ Constructor """

        api_base = api_base if api_base else self.__API_BASE
        super(EI3, self).__init__(cas, EI3.__APP_NAME,
                                  api_host=host if host else self.__HOST,
                                  api_base=api_base if api_base else self.__API_BASE,
                                  shiro_cas_base=shiro_cas_base if shiro_cas_base else self.__SHIRO_CAS_BASE)

    # Band category
    def get_band_categories(self):
        res = self.request_get('/bandcategory')
        return [BandCategory.from_dict(x) for x in res['data']]

    def add_band_category(self, band_category):
        assert band_category and isinstance(band_category, BandCategory)
        res = self.request_post_form('/bandcategory', band_category.to_simple())
        self._logger.debug(res)
        return BandCategory.from_dict(res['data'])

    def update_band_category(self, band_category):
        assert band_category and isinstance(band_category, BandCategory)
        band_category_id = band_category['id']
        assert band_category_id
        res = self.request_post_form('/bandcategory/{0}'.format(band_category_id), band_category.to_simple())
        return BandCategory.from_dict(res['data'])

    def del_band_category(self, band_category):
        assert band_category
        band_category_id = band_category['id'] if isinstance(band_category, BandCategory) else band_category
        assert band_category_id
        res = self.request_del('/bandcategory/{0}'.format(band_category_id))
        return res['data']

    # Band #
    def add_band(self, band, file_path=None):
        assert band and isinstance(band, Band)
        band_category_id = band['categoryId']
        if file_path:
            assert band['type'] == BandType.UPLOAD
            res = self.request_upload('/band', band, file_path)
        else:
            res = self.request_post_multipart('/band', band)
        return Band.from_dict_with_ext_cat_id(res['data'], band_category_id)

    def update_band(self, band, file_path=None):
        assert band and isinstance(band, Band)
        band_category_id = band['categoryId']
        band_id = band['id']
        assert band_id
        if file_path:
            assert band['type'] == BandType.UPLOAD
            res = self.request_upload('/band/{0}'.format(band_id), band, file_path)
        else:
            res = self.request_post_multipart('/band/{0}'.format(band_id), band)
        return Band.from_dict_with_ext_cat_id(res['data'], band_category_id)

    def del_band(self, band):
        assert band
        band_id = band['id'] if isinstance(band, Band) else band
        assert band_id
        res = self.request_del('/band/{0}'.format(band_id))
        return res['data']

    # Fixed (external) gene
    def get_fixed_gene_categories(self):
        res = self.request_get('/fixedgenecategory')
        return [FixedGeneCategory.from_dict(x) for x in res['data']]

    def upload_fixed_gene_schema(self, group, file_path):
        """ Upload fixed (external) gene schema (admin/operator only) """
        assert group and file_path
        group_id = group['id'] if isinstance(group, Group) else int(group)
        res = self.request_upload('/fixedgene/schema', {'groupId': group_id}, file_path)
        return FixedGeneCategory.from_dict(res['data'])

    def upload_fixed_gene_data(self, group, file_path):
        """ Upload fixed (external) gene data (admin/operator only) """
        assert group and file_path
        group_id = group['id'] if isinstance(group, Group) else int(group)
        res = self.request_upload('/fixedgene/data', {'groupId': group_id}, file_path)
        return res['data']
