def create_html(timeline_items,
                config_types_json='{"grey": {"bg": "#c2c2d6", "fg": "black"}, "blue": {"bg": "#006080", "fg": "white"}, "green": {"bg": "#008000", "fg": "white"}, "red": {"bg": "#ff704d", "fg": "white"}}',
                config_max_zoom_seconds='auto'):
    """
    exmaple:
        from press.vis import timeline
        import press
        from datetime import datetime
        import random
        import json

        # defining coloring types <type-name: foreground/background HTML valid color
        colortypes = {  'grey':dict(bg='#804000', fg='white'),  'blue':dict(bg='blue', fg='white'),
                'green': dict(bg='#006622', fg='white'),
                'red': dict(bg='#ff704d', fg='white')}
        colorkeys = list(colortypes.keys())
        data = [dict(dt=datetime(2019,3,27,random.randint(1,23),random.randint(0,59)),str='item {}'.format(i),type=colorkeys[i%len(colorkeys)]) for i in range(20)]
        r = press.Report('Timeline demonstration', 'show time')
        r.attach(timeline.create_html(data, config_types_json=json(colortypes), config_max_zoom_seconds=60*60*12)
        r.show()

    :param timeline_items:
    :return:
    """
    import uuid
    import json
    import warnings

    assert isinstance(timeline_items, (list, tuple))

    timeline_items = sorted(timeline_items, key=lambda xi: xi['start_dt'])

    if config_max_zoom_seconds == 'auto':
        try:
            config_max_zoom_seconds = (timeline_items[-1]['end_dt' if 'end_dt' in timeline_items[-1] else 'start_dt'] - timeline_items[0]['start_dt']).total_seconds()
        except Exception as e:
            config_max_zoom_seconds = 60*60*12
            warnings.warn('Failed to auto config max-zoom-time ({msg}): fallback to default max zoom ({val}) seconds'.format(msg=e, val=config_max_zoom_seconds))

    item_classes = json.loads(config_types_json)

    unique_id = str(uuid.uuid4()).replace('-', '_')

    def _item_class_style():
        if item_classes:
            _content = '.vis-item.foo {} ' + ' '.join([".vis-item.{c} {{background-color: {bg}; color: {fg}; border-color: black;}}"
                                                      .format(c=c, bg=item_classes[c]['bg'], fg=item_classes[c]['fg']) for c in item_classes])
            return """
                '<style type="text/css">{}</style>'
            """.format(_content)
        else:
            return "''"

    js_items = ["{{'start':'{start_dt}',{op_end_dt} 'content':'{txt}', 'className':'{c}'}}".format(start_dt=x['start_dt'],
                                                                                                   op_end_dt="'end':'{end_dt}',".format(end_dt=x['end_dt']) if 'end_dt' in x else '',
                                                                      txt=x['text'],
                                                                      c=x['type'] if item_classes and
                                                                                     'type' in x and
                                                                                     x['type'] in item_classes else 'default') for x in timeline_items]
    iistyle= _item_class_style()
    return """
    <!--div id="mytimeline" style="background-color: #FAFAFA;"></div-->

    <div id="visualization_{unique_id}" style="width: 100%;box-sizing: border-box;"></div>

    <script type="text/javascript">
        function makevisvis(container_id, item_list){{
            var container = document.getElementById(container_id);
            // note that months are zero-based in the JavaScript Date object
            var items = new vis.DataSet(item_list);
            var options = {{
                    // Set global item type. Type can also be specified for items individually
                    // Available types: 'box' (default), 'point', 'range'
                    //type: 'point',
                    //showMajorLabels: false
                    zoomMax: {zoommax},
                    zoomMin: 500
                    
                }};
            var timeline = new vis.Timeline(container, items, options);
        }}
        
        if (!document.getElementById('vislib')){{
        
        var head= document.getElementsByTagName('head')[0];

        function loadcss(url) {{
           // var head = document.getElementsByTagName('head')[0],
           link = document.createElement('link');
           link.type = 'text/css';
           link.rel = 'stylesheet';
           link.href = url;
           head.appendChild(link);
           
           return link;
        }}   
        
        function addCssToDocument(css){{
            var style = document.createElement('style')
            style.innerText = css
            document.head.appendChild(style)
        }}      
        
        addCssToDocument({a});       

        var script= document.createElement('script');
        script.type= 'text/javascript';
        script.id = 'vislib';
        script.src= 'https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis.js';
        script.onreadystatechange= function () {{
                if (this.readyState == 'complete') {{ loadcss("https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis-timeline-graph2d.min.css");
                makevisvis('visualization_{unique_id}', [ {items} ]); }}
        }}
        script.onload=()=>{{loadcss("https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis-timeline-graph2d.min.css"); 
        makevisvis('visualization_{unique_id}', [ {items} ]);}}
        head.appendChild(script);        
        }} else {{
            document.getElementById('vislib').addEventListener("load", ()=>{{makevisvis('visualization_{unique_id}', [ {items} ])}});
        }}
        
    </script>
    """.format(items=','.join(js_items), a=iistyle, unique_id=unique_id, zoommax=config_max_zoom_seconds*1000)

