import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
from matplotlib import dates as mpl_dates

months=['January','February','March','April','May','June','July','August','September','October','November','December']

# Import data
df = pd.read_csv('fcc-forum-pageviews.csv', index_col='date', parse_dates=True)

# Clean the data
f25 = df['value'] <= df['value'].quantile(0.025)
f75 = df['value'] >= df['value'].quantile(0.975)
cond = (f25 | f75)
df = df.drop(index=df[cond].index)

def draw_line_plot():
    fig, ax = plt.subplots()
    fig.set_figwidth(16)
    fig.set_figheight(6)

    ax.plot_date(df.index, df['value'], linestyle='solid', marker=None, color="green")
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    # put ticker every 6 months
    ax.xaxis.set_major_locator(ticker.MultipleLocator(180))
    ax.xaxis.set_major_formatter(mpl_dates.DateFormatter('%Y-%m'))

    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.strftime('%B')
    df_grp = df_bar.groupby(['year', 'month'])
    df_grp['value'].apply(lambda x: x.mean())

    sns.set_style("ticks")
    g = sns.catplot(x="year", y="value", kind="bar", hue="month", data=df_bar, hue_order=months, ci=None, legend=None, palette="twilight")

    fig, ax = g.fig, g.ax
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    plt.xticks(rotation=90)
    plt.legend(loc='upper left', title="Month")
    plt.setp(ax.get_legend().get_texts(), fontsize='8')
    plt.setp(ax.get_legend().get_title(), fontsize='8')
    plt.tight_layout()
    
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    df_box = df.copy()
    df_box['year'] = [d.year for d in df_box.index]
    df_box['month'] = [d.strftime('%b') for d in df_box.index]

    # adjust data
    df_box.sort_values(by=['year','date'], ascending=[False, True], inplace=True)

    df_box['Page Views'] = df_box['value']
    df_box['Month'] = df_box['month']
    df_box['Year'] = df_box['year']
    g = sns.PairGrid(df_box, x_vars=['Year', 'Month'], y_vars=['Page Views'], palette='twilight')
    g.map(sns.boxplot)
    fig = g.fig
    
    fig.set_figheight(6)
    fig.set_figwidth(16)
    fig.axes[0].set_ylabel('Page Views')
    fig.axes[1].set_ylabel('Page Views')
    fig.axes[0].set_title('Year-wise Box Plot (Trend)')
    fig.axes[1].set_title('Month-wise Box Plot (Seasonality)')
    plt.tight_layout()
    
    fig.savefig('box_plot.png')
    return fig