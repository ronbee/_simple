

def test_pass():
    import press
    import matplotlib.pyplot as plt
    import numpy as np

    # scatter.py

    from bokeh.plotting import figure
    from bokeh.models import Range1d

    # Data for plotting
    t = np.arange(0.0, 2.0, 0.01)
    s = 1 + np.sin(2 * np.pi * t)

    # Note that using plt.subplots below is equivalent to using
    # fig = plt.figure and then ax = fig.add_subplot(111)
    fig, ax = plt.subplots()
    ax.plot(t, s)

    ax.set(xlabel='time (s)', ylabel='voltage (mV)',
           title='basic figure')
    ax.grid()

    r = press.Report('testing package with matplotlib')
    r.attach('## Figure')
    r.attach('---')
    r.attach(fig)

    r.attach("""<div class ="container">
                    <h2>Select:</h2>
                    <div id="selected_form_code">
                    <select id="select_btn">
                        <option>one</option>
                        <option>two</option>
                    </select></div>""")


    # create some data
    x1 = range(11)
    y1 = [0, 8, 2, 4, 6, 9, 5, 6, 25, 28, 4, 7]

    # select the tools we want
    TOOLS = "pan,box_zoom,reset,save"

    # the red and blue graphs will share this data range
    xr1 = Range1d(start=0, end=30)
    yr1 = Range1d(start=0, end=30)

    # build our figures
    p1 = figure(x_range=xr1, y_range=yr1, tools=TOOLS, plot_width=350, plot_height=310)
    p1.scatter(x1, y1, size=12, color="blue", alpha=0.4)

    r.attach(p1)

    r.html()

    r.show('press-report.html')

    assert True, "sample test"
