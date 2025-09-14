library(ggplot2)
library(tidyr)
library(dplyr)
library(readr)
library(tibble)
library(forcats)
library(patchwork)

# Load matrix
df <- read_csv("/Users/aidanjones/Desktop/best_residues_matrix_final.csv")

# Genes to include
genes_to_include <- c("PAL", "C4H", "4CL", "CHS", "CHI1", "F3H", "F3-H", "F3-5-H", "FLS", "DFR", "ANS", "TT19", "BZ2", "MYB113", "MYBPl/C1", "LAR", "ANR", "MYB123")

# Filter relevant columns
df_filtered <- df %>%
  select(Species, all_of(genes_to_include))

# BUSCO values
busco_values <- c(
  "Acorus_calamus" = 89.7,
  "Spirodela_intermedia" = 95.3,
  "Discorea_alata" = 96.5,
  "Dendrobium_catenatum" = 78.1,
  "Musa_acuminata" = 98.8,
  "Ananas_comosus" = 97.9,
  "Eragrostis_tef" = 95.4,
  "Panicum_miliaceum" = 92.0,
  "Zea_mays" = 96.0,
  "Miscanthus_lutarioriparius" = 94.1,
  "Oryza_rufipogon" = 90.2,
  "Phyllostachys_edulis" = 92.3,
  "Stipa_capillata" = 97.0,
  "Brachypodium_arbuscula_BARB1" = 96.7,
  "Brachypodium_distachyon_Bd21" = 97.1,
  "Brachypodium_distachyon_ABR2" = 94.6,
  "Brachypodium_distachyon_ABR3" = 94.0,
  "Brachypodium_distachyon_ABR6" = 73.3,
  "Brachypodium_distachyon_Arn1" = 94.9,
  "Brachypodium_distachyon_Bd29-1" = 87.4,
  "Brachypodium_distachyon_BdTR10h" = 82.1,
  "Brachypodium_distachyon_BdTR13k" = 80.7,
  "Brachypodium_distachyon_BdTR5i" = 88.0,
  "Brachypodium_distachyon_Bis-1" = 93.2,
  "Brachypodium_hybridum_118-5" = 97.7,
  "Brachypodium_hybridum_118-8" = 98.4,
  "Brachypodium_hybridum_ABR113" = 97.5,
  "Brachypodium_hybridum_Bd28" = 97.6,
  "Brachypodium_hybridum_Bhyb127-1" = 98.5,
  "Brachypodium_hybridum_Bhyb26" = 97.8,
  "Brachypodium_hybridum_IBd483" = 98.5,
  "Brachypodium_hybridum_v30" = 97.6,
  "Brachypodium_mexicanum_813" = 97.5,
  "Brachypodium_stacei_ABR114" = 96.8,
  "Brachypodium_stacei_Bst99" = 97.7,
  "Brachypodium_sylvaticum_Ain-1" = 97.0,
  "Bromus_sterilis" = 97.0,
  "Aegilops_tauschii" = 97.3,
  "Campeiostachys_nutans" = 97.6,
  "Hordeum_marinum" = 92.8,
  "Secale_cereale" = 94.2,
  "Thinopyrum_intermedium" = 98.0,
  "Triticum_aestivum" = 98.0,
  "Alopecerus_aequalis" = 97.2,
  "Avena_insularis" = 95.7,
  "Beckmannia_syzigachne" = 97.2,
  "Dactylis_glomerata" = 97.1,
  "Lolium_perenne" = 97.3,
  "Puccinellia_tenuiflora" = 87.4,
  "Coptis_chinensis" = 78.8,
  "Nelumbo_nucifera" = 98.8,
  "Vitis_rotundifolia" = 83.8,
  "Vicia_villosa" = 99.6,
  "Ziziphus_jujuba" = 99.7,
  "Quercus_lobata" = 98.5,
  "Ricinus_communis" = 99.8,
  "Citrus_clementina" = 99.5,
  "Punica_granatum" = 99.4,
  "Cardamine_hirsuta" = 95.9,
  "Durio_zibethinus" = 98.9,
  "Cornus_florida" = 99.5,
  "Actinidia_eriantha" = 97.9,
  "Oldenlandia_corymbosa" = 96.0,
  "Andrographis_paniculata" = 99.0,
  "Lycium_barbarum" = 99.6,
  "Artemisia_annua" = 88.3,
  "Lonicera_japonica" = 76.2

)

# Define species order and taxonomic groups
species_groups <- tibble::tribble(
  ~Species,                            ~Order,            ~Classification,
  "Acorus_calamus",                    "Acorales",        "Monocot",
  "Spirodela_intermedia",              "Alismatales",     "Monocot",
  "Discorea_alata",                    "Dioscoreales",    "Monocot",
  "Dendrobium_catenatum",              "Asparagales",     "Monocot",
  "Musa_acuminata",                    "Zingiberales",    "Monocot",
  "Ananas_comosus",                    "Poales",          "Monocot",
  "Eragrostis_tef",                    "Poales",          "Poaceae",
  "Panicum_miliaceum",                 "Poales",          "Poaceae",
  "Zea_mays",                          "Poales",          "Poaceae",
  "Miscanthus_lutarioriparius",        "Poales",          "Poaceae",
  "Oryza_rufipogon",                   "Poales",          "Poaceae",
  "Phyllostachys_edulis",              "Poales",          "Poaceae",
  "Stipa_capillata",                   "Poales",          "Poaceae",
  "Brachypodium_arbuscula_BARB1",      "Poales",          "Poaceae",
  "Brachypodium_distachyon_Bd21",      "Poales",          "Poaceae",
  "Brachypodium_distachyon_ABR2",      "Poales",          "Poaceae",
  "Brachypodium_distachyon_ABR3",      "Poales",          "Poaceae",
  "Brachypodium_distachyon_ABR6",      "Poales",          "Poaceae",
  "Brachypodium_distachyon_Arn1",      "Poales",          "Poaceae",
  "Brachypodium_distachyon_Bd29-1",    "Poales",          "Poaceae",
  "Brachypodium_distachyon_BdTR10h",   "Poales",          "Poaceae",
  "Brachypodium_distachyon_BdTR13k",   "Poales",          "Poaceae",
  "Brachypodium_distachyon_BdTR5i",    "Poales",          "Poaceae",
  "Brachypodium_distachyon_Bis-1",     "Poales",          "Poaceae",
  "Brachypodium_hybridum_118-5",       "Poales",          "Poaceae",
  "Brachypodium_hybridum_118-8",       "Poales",          "Poaceae",
  "Brachypodium_hybridum_ABR113",      "Poales",          "Poaceae",
  "Brachypodium_hybridum_Bd28",        "Poales",          "Poaceae",
  "Brachypodium_hybridum_Bhyb127-1",   "Poales",          "Poaceae",
  "Brachypodium_hybridum_Bhyb26",      "Poales",          "Poaceae",
  "Brachypodium_hybridum_IBd483",      "Poales",          "Poaceae",
  "Brachypodium_hybridum_v30",         "Poales",          "Poaceae",
  "Brachypodium_mexicanum_813",        "Poales",          "Poaceae",
  "Brachypodium_stacei_ABR114",        "Poales",          "Poaceae",
  "Brachypodium_stacei_Bst99",         "Poales",          "Poaceae",
  "Brachypodium_sylvaticum_Ain-1",     "Poales",          "Poaceae",
  "Bromus_sterilis",                   "Poales",          "Poaceae",
  "Aegilops_tauschii",                 "Poales",          "Poaceae",
  "Campeiostachys_nutans",             "Poales",          "Poaceae",
  "Hordeum_marinum",                   "Poales",          "Poaceae",
  "Secale_cereale",                    "Poales",          "Poaceae",
  "Thinopyrum_intermedium",            "Poales",          "Poaceae",
  "Triticum_aestivum",                 "Poales",          "Poaceae",
  "Alopecerus_aequalis",               "Poales",          "Poaceae",
  "Avena_insularis",                   "Poales",          "Poaceae",
  "Beckmannia_syzigachne",             "Poales",          "Poaceae",
  "Dactylis_glomerata",                "Poales",          "Poaceae",
  "Lolium_perenne",                    "Poales",          "Poaceae",
  "Puccinellia_tenuiflora",            "Poales",          "Poaceae",
  "Coptis_chinensis",                  "Ranunculales",    "Eudicot",
  "Nelumbo_nucifera",                  "Proteales",       "Eudicot",
  "Vitis_rotundifolia",                "Vitales",         "Eudicot",
  "Vicia_villosa",                     "Fabales",         "Eudicot",
  "Ziziphus_jujuba",                   "Rosales",         "Eudicot",
  "Quercus_lobata",                    "Fagales",         "Eudicot",
  "Ricinus_communis",                  "Malpighiales",    "Eudicot",
  "Citrus_clementina",                 "Sapindales",      "Eudicot",
  "Punica_granatum",                   "Myrtales",        "Eudicot",
  "Cardamine_hirsuta",                 "Brassicales",     "Eudicot",
  "Durio_zibethinus",                  "Malvales",        "Eudicot",
  "Cornus_florida",                    "Cornales",        "Eudicot",
  "Actinidia_eriantha",                "Ericales",        "Eudicot",
  "Oldenlandia_corymbosa",             "Gentianales",     "Eudicot",
  "Andrographis_paniculata",           "Lamiales",        "Eudicot",
  "Lycium_barbarum",                   "Solanales",       "Eudicot",
  "Artemisia_annua",                   "Asterales",       "Eudicot",
  "Lonicera_japonica",                 "Dipsacales",      "Eudicot",

) %>%
  mutate(BUSCO = busco_values[Species])

# Join taxonomy into matrix
df_annotated <- df_filtered %>%
  inner_join(species_groups, by = "Species")

# Long format & filtering
df_long <- df_annotated %>%
  pivot_longer(cols = all_of(genes_to_include), names_to = "Gene", values_to = "ConservedResidues") %>%
  mutate(
    ConservedResidues = as.numeric(ConservedResidues),
    ConservedResidues = ifelse(ConservedResidues >= 75, ConservedResidues, NA),
    ConservedResidues = ifelse((Classification %in% c("Monocot", "Eudicot") & Gene == "BZ2"), NA, ConservedResidues),
    ConservedResidues = ifelse((Classification == "Poaceae" & Gene == "TT19"), NA, ConservedResidues)
  )

# Set consistent factor levels
species_levels <- rev(species_groups$Species)
df_long$Species <- factor(df_long$Species, levels = species_levels)
df_annotated$Species <- factor(df_annotated$Species, levels = species_levels)
df_long$Classification <- factor(df_long$Classification, levels = c("Monocot", "Poaceae", "Eudicot"))
df_annotated$Classification <- factor(df_annotated$Classification, levels = c("Monocot", "Poaceae", "Eudicot"))
df_long$Gene <- factor(df_long$Gene, levels = genes_to_include)

# Heatmap plot
matrix_plot <- ggplot(df_long, aes(x = Gene, y = Species, fill = ConservedResidues)) +
  geom_tile(color = "grey80", size = 0.5) +
  scale_fill_gradient(
    low = "grey80", high = "black",
    na.value = "white", limits = c(75, 100),
    name = "Conserved\nResidues (%)"
  ) +
  # Replace underscores and set italic labels
  scale_y_discrete(
    position = "left",
    labels = function(x) gsub("_", " ", x)
  ) +
  facet_grid(rows = vars(Classification), scales = "free_y", space = "free_y") +
  theme_minimal() +
  theme(
    axis.text.x = element_text(angle = 90, hjust = 1),
    panel.grid = element_blank(),
    axis.text.y = element_text(
      size = 6,
      hjust = 1,
      face = "italic"
    ),
    strip.text.y = element_text(angle = 0),
    strip.placement = "outside",
    strip.background = element_blank(),
    axis.line.y = element_line(),
    axis.ticks.y = element_line()
  ) +
  labs(
    title = "Presence-Absence Matrix",
    x = "Gene",
    y = "Species"
  )

# BUSCO bar plot aligned with tiles
busco_plot <- ggplot(df_annotated, aes(y = Species)) +
  geom_segment(aes(x = 70, xend = 100, y = Species, yend = Species),
               color = "grey80", size = 0.4) +
  geom_tile(aes(x = BUSCO - (BUSCO - 70)/2, width = BUSCO - 70, height = 0.9, fill = Classification)) +
  geom_text(aes(x = 69, label = sprintf("%.1f", BUSCO)),
            hjust = 1, size = 2.5) +
  scale_fill_manual(
    values = c(
      "Monocot" = "#FFD04A",
      "Poaceae" = "#C0C0DF",
      "Eudicot" = "#69D946"
    ),
    guide = "none"  # Hide legend for BUSCO bars
  ) +
  scale_x_continuous(limits = c(50, 105), expand = c(0, 0)) +
  facet_grid(rows = vars(Classification), scales = "free_y", space = "free_y") +
  theme_minimal() +
  theme(
    axis.title = element_blank(),
    axis.text.y = element_blank(),
    axis.ticks.y = element_blank(),
    axis.text.x = element_blank(),
    axis.ticks.x = element_blank(),
    panel.grid = element_blank(),
    strip.text.y = element_blank(),
    strip.background = element_blank(),
    plot.margin = margin(5, 5, 5, 0)
  )

# Combine plots
final_plot <- matrix_plot + busco_plot + plot_layout(widths = c(3, 1))

# Save plot
ggsave(
  filename = "/Users/aidanjones/Desktop/presence_absence_matrix_with_busco.pdf",
  plot = final_plot,
  width = 10,
  height = 8,
  dpi = 300
)

print(final_plot)