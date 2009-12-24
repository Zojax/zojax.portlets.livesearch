/* zojax live search portlet */

Ext.onReady(function(){

    var el = Ext.get('z-portlet-livesearch-field');
    if (!el) {
	return;
    }

    var ds = new Ext.data.Store({
        proxy: new Ext.data.ScriptTagProxy({
            url: '++portlet++portlet.livesearch/search.html'
        }),
        reader: new Ext.data.JsonReader({
            id: 'id',
            root: 'result',
            totalProperty: 'totalCount'
        }, [
            {name: 'title', mapping: 'title'},
            {name: 'url', mapping: 'url'},
	    {name: 'icon', mapping: 'icon'},
            {name: 'owner', mapping: 'owner'},
            {name: 'modified', mapping: 'modified'},
	    {name: 'description', mapping: 'description'},
        ])
    });

    // Custom rendering template
    var resultTpl = new Ext.XTemplate(
        '<tpl for="."><div class="z-portlet-livesearch-item" style="padding:0.5em">',
	'<div style="float: left; padding-right: 0.5em">{icon}</div>',
        '<h2 class="strong">{title}</h2>',
	'<div class="discreet">by {owner}, {modified}</div>',
        '<div style="padding-bottom: 1em">{description}</div>',
        '</div></tpl>'
    );

    var search = new Ext.form.ComboBox({
        store: ds,
        displayField: 'title',
        typeAhead: false,
        loadingText: 'Searching...',
        pageSize: 10,
        hideTrigger: true,
	listWidth: 320,
	listAlign: 'tr-br',
        tpl: resultTpl,
        applyTo: 'z-portlet-livesearch-field',
        itemSelector: 'div.z-portlet-livesearch-item',
        onSelect: function(record){
            window.location = record.data.url;
        }
    });
});
