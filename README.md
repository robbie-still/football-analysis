# football-analysis

This repository will contain my random collection of R and Python templates for football data analysis and visualisations. 

## Examples

### ggplot theme - see [this folder](https://github.com/robbiestill/football-analysis/blob/master/R/ggplot/scatter_template) for full code. 

```{r,echo=TRUE, message=FALSE}

ggplot(data, aes(x= PassCompletion, y= xAper90, label=player, 
                       col = colour))+
  geom_text_repel(
    aes(label=ifelse(xAper90>0.5|PassCompletion>87|player == "Bruno Fernandes",
                     as.character(player),'')),
    box.padding = 1, 
    col = text_colour, 
    alpha = 0.5
  ) +
  geom_point() +
  scale_color_manual(values = c("primary" = primary, "secondary" =
                                  secondary, "filler" = filler)) +
  theme_rs() + 
  theme(legend.position = "none") + 
  labs(title = paste0("<span style='font-family:",title_font,
    "'>Elite playmakers: <span style='color:", 
    primary,";'>high</span> or <span style='color:",secondary,
    ";'>low</span> risk passing profiles </span>"), 
    subtitle = "Data from Infogol, Domestic Leagues 2019/20") +
  xlab("Pass Completion (%)") +
  ylab("Expected Assists Per 90") +
  annotation_custom(logo, xmin = 89, xmax = 90.5, ymin = 0.85, ymax = 0.98) +
  coord_cartesian(clip = "off") 
```

![](https://raw.githubusercontent.com/robbiestill/football-analysis/master/R/ggplot/playmakers-new.jpeg)

### python theme and radar plot - see [this script](https://github.com/robbiestill/football-analysis/blob/master/Python/radar_template.py)

```{python}
# create plot
fig1 = plt.figure(figsize=(6, 6))
fig1.set_facecolor(background)
radar = ComplexRadar(fig1, variables, ranges, 6)
radar.plot(playerone, color = primary, zorder =2)
radar.fill(playerone, alpha=0.3, color = primary, zorder =2)
radar.plot(playertwo, color = secondary, zorder =2)
radar.fill(playertwo, alpha=0.5, color = secondary, zorder =2)

# add highlighted title 
s = "Comparing <{}> with <{}>\n"
htext.fig_htext(s.format(columnsNamesArr[1],columnsNamesArr[2]),0.16,1.12,highlight_colors=[primary, secondary],
                highlight_weights=["bold"],string_weight="bold",fontsize=14,
                fontfamily=title_font,color=text_colour)
fig1.text(0.16,1.12,"English Premier League "+df.iloc[0,1],fontweight="regular",fontsize=14,
         color=text_colour, fontfamily=title_font)
# add logo
ax2=fig1.add_axes([0,1.05,0.2,0.2])
ax2.axis("off")
url = "https://logos-world.net/wp-content/uploads/2020/05/Arsenal-Logo.png"
response = requests.get(url)
img = Image.open(BytesIO(response.content))
ax2.imshow(img)

#add credit 
fig1.text(0, -0.025, "Created by Robbie Still / @datarobbie1. Data provided by WhoScored.com",
                       fontstyle="italic", fontsize=9, fontfamily=title_font, color=text_colour)

```
![](https://raw.githubusercontent.com/robbiestill/football-analysis/master/Python/Hector%20Bellarin%20and%20Ainsley%20Maitland-Niles.jpg)
