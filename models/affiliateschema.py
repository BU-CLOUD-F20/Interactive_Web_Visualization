from run import ma

class AffiliateSchema(ma.Schema):
    class Meta:
        fields = ('title', 'authors', 'scopusIds', 'year', 'citations', 'weight')