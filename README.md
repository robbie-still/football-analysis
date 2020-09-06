# football-analysis

This repository will contain my random collection of R and Python templates for football data analysis and visualisations. 

## Examples


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


