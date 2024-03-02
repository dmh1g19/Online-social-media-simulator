from dash import html


def get_help_info():
    helpful_info = html.Div([
        html.H3("Helpful Information"),
        html.P("Here you can find some useful information about how to navigate the application and interpret the data."),

        html.H3("Parameters"),
        html.Li("Theta:"),
        html.P("Deception parameter, defined as the probability that bad actor content is irresistible"),
        html.Li("Gamma:"),
        html.P("Amount of influence of inauthentic nodes (how any inauthentic nodes are followed by authentic ones, aka 'infiltration"),
        html.Li("Beta:"),
        html.P("Number of inauthentic nodes in relation to authentic"),
        html.P("Authentic users have quality qual to its engagement."),
        html.P("Inauthentic users have higher engagement content."),

        html.H3("Engagement:"),
        html.P("This parameter refers to a message's ability to attract attention from a node in order to incrase the chances of resharing."),
        
        html.Li("Quality:"),
        html.P("Refers to a massages quality, such that authentic users have set to have a high quality and inauthentic users have a very low quality."),

        html.H3("Message timelines"),
        html.P("Each user has an individual timeline of messages with a maximum capacity, old messages are replaced by newer ones, simulating reslistic dynamic exposure to content."),
        
        html.H3("Message resharing (POLLING)"),
        html.P("Messages are shared based on their relative engagement to the total engagement of all messages in an agent's feed."),
        html.P("This approach reflects a more nuanced understanding of how engagement influences information spread, where messages compete for attention based on their appeal."),
        html.P("The assumption that content produced by bots is of strictly low quality, focusing on the distinction between the intrinsic value (quality) of information and its perceived appeal or engagement. The engagement of these messages can be manipulated through deception to be higher, but the quality remains low, emphasizing the bots' role in spreading low-quality, potentially misleading information within the network."),
    ])

    return helpful_info
