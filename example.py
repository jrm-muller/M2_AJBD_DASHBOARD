import numpy as np
import plotly.graph_objects as go

fig=go.Figure().set_subplots(2,1, vertical_spacing=0.05,
                             specs=[[{"type": "polar"}], [{"type":"bar"}]])

r=[3.5, 1.5, 2.5, 4.5, 4.5, 4, 3]
theta=[65, 15, 210, 110, 312.5, 180, 270]
width=[20,15,10,20,15,30,15]
x= np.arange(1, 8)
bh = [4, 6, 3, 7, 8, 5, 9]


fig.add_trace(go.Barpolar(r=r[:1], theta=theta[:1], width=width[:1],
                          marker_color="#ff8c00",
                          marker_line_color="black",
                          marker_line_width=1),1, 1)
fig.add_trace(go.Bar(x=x[:1], y=bh[:1], marker_color="green", width=0.95), 2,1);

fig.update_layout(width=800, height=700, xaxis_range=[0.5, 7.5], yaxis_range=[0, max(bh)+0.5]);

frames=[go.Frame(data=[go.Barpolar(r=r[:k+1], theta=theta[:k+1], width=width[:k+1]),
                       go.Bar(x=x[:k+1], y=bh[:k+1])],
                 name=f"fr{k}",
                 traces=[0,1]) for k in range(len(r))]  #r, theta, width, x, bh must have the same len=number of frames

fig.update(frames=frames)

def frame_args(duration):
    return {
            "frame": {"duration": duration},
            "mode": "immediate",
            "fromcurrent": True,
            "transition": {"duration": duration, "easing": "linear"},
        }

fr_duration=50  # customize this frame duration according to your data!!!!!
sliders = [
            {
                "pad": {"b": 10, "t": 50},
                "len": 0.9,
                "x": 0.1,
                "y": 0,
                "steps": [
                    {
                        "args": [[f.name], frame_args(fr_duration)],
                        "label": f"fr{k+1}",
                        "method": "animate",
                    }
                    for k, f in enumerate(fig.frames)
                ],
            }
        ]


fig.update_layout(sliders=sliders,
                  updatemenus = [
                        {
                        "buttons": [
                            {
                             "args": [None, frame_args(fr_duration)],
                             "label": "&#9654;", # play symbol
                             "method": "animate",
                            },
                            {
                             "args": [[None], frame_args(fr_duration)],
                             "label": "&#9724;", # pause symbol
                             "method": "animate",
                            }],
                        "direction": "left",
                        "pad": {"r": 10, "t": 70},
                        "type": "buttons",
                        "x": 0.1,
                        "y": 0,
                        }])
fig.show()
