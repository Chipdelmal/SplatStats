###############################################################################
# Color Constants (source: https://splatoonwiki.org/wiki/Ink#Color_Lock_3)
#   The use of a VSCode extension like "Color Highlight" is highly 
#   recommended to explore this file.
###############################################################################
from random import shuffle
import matplotlib.colors as mcolors

###############################################################################
# Splatoon 1
###############################################################################
# Regular Battle --------------------------------------------------------------
PINK_V_GREEN_S1             = ('#C83D79', '#409D3B', '#2BDCED')
PINK_V_TURQUOISE_S1         = ('#C93457', '#048188', '#890B5D')
PINK_V_ORANGE_S1            = ('#DA3781', '#ED9408', '#A577FF')
ORANGE_V_BLUE_S1            = ('#CF581B', '#141494', '#FFFF00')
GREEN_V_PURPLE              = ('#799516', '#6E068A', '#118991')
TURQUOISE_V_ORANGE_S1       = ('#20837D', '#DF641A', '#AD7710')
LBLUE_V_ORANGE_S1           = ('#228CFF', '#E85407', '#EFF66E')
LBLUE_V_YELLOW              = ('#007EDC', '#E1A307', '#D01D79')
BLUE_V_ORANGE               = ('#2E0CB5', '#F86300', '#FDFF00')
BLUE_V_LIME                 = ('#26229F', '#91B00B', '#FF7F19')
# Ranked Battle ---------------------------------------------------------------
YELLOW_V_LILAC_S1           = ('#DD9016', '#4D24A3', '#A1E896')
GREEN_V_MAGENTA_S1          = ('#79B726', '#A52B85', '#ECC50A')
LUMIGREEN_V_PURPLE_S1       = ('#60AB43', '#891A7F', '#FFB500')
LGREEN_V_BLUE_S1            = ('#8CE47F', '#3D59DE', '#FFA427')
SODA_V_PURPLE_S1            = ('#65B799', '#9736B2', '#8ED11E')
GREEN_V_ORANGE_S1           = ('#319471', '#BF3E24', '#B986ED')
DBLUE_V_YELLOW_S1           = ('#0D195E', '#B97E1A', '#FF5937')
# Octovalley ------------------------------------------------------------------
ORANGE_V_DFUCHSIA_S1        = ('#FF6C00', '#6C0676', '#FFE500')
NMARIGOLD_V_DFUCHSIA_S1     = ('#D88602', '#5C0A61', '#05E7CE')
MARIGOLD_V_DFUCHSIA_S1      = ('#EEAA05', '#8C0C7F', '#17774F')
YELLOW_V_DFUCHSIA_S1        = ('#FBD704', '#8C0C7F', '#1BC3D8')
GREEN_V_DFUCHSIA_S1         = ('#8EBB1A', '#8C0C7F', '#FFE500')
BGREEN_V_DFUCHSIA_S1        = ('#6ABF0B', '#8C0C7F', '#FFE500')
LUMIGREEN_V_DFUCHSIA_S1     = ('#2D9314', '#8C0C7F', '#005BFF')
NLUMIGREEN_V_DFUCSHIA_S1    = ('#09950B', '#8C0C7F', '#005BFF')
MOTHGREEN_V_DFUCSHIA_S1     = ('#425113', '#8C0C7F', '#FFE500')
SODA_V_DFUCSHIA_S1          = ('#8EDBB8', '#8C0C7F', '#FFE500')
TURQUOISE_V_DFUCSHIA_S1     = ('#0DA182', '#8C0C7F', '#FFE500')
LILAC_V_DFUCSHIA_S1         = ('#525CF5', '#8C0C7F', '#FFE500')
DBLUE_V_DFUCSHIA_S1         = ('#0D37C3', '#941A88', '#6BFF00')
# Splatfest -------------------------------------------------------------------
CATS_V_DOGS_S1              = ('#D84011', '#41A782')
RCOASTER_V_WSLIDE_S1        = ('#3BC335', '#B400FF')
MARSHMALLOW_V_HDOG_S1       = ('#CE334F', '#008006', '#FFE80A')
NPOLE_V_SPOLE               = ('#801AB3', '#03C1CD', '#E6B30D')
LEMONT_V_MILKT              = ('#E59D0D', '#E1D6B6')
AUTOBOTS_V_DECEPTICONS      = ('#EC0B68', '#461362')
MESSY_V_TIDY                = ('#ED7004', '#0037B8')
PIRATES_V_NINJAS            = ('#4F9E00', '#7D26B5')
NAUGHTY_V_NICE_S1           = ('#CF3350', '#008040')
PAST_V_FUTURE_S1            = ('#009A82', '#A34C3B')
BARBARIAN_V_NINJA_S1        = ('#C54D4F', '#003B89')
PBODY_V_PBRAIN_S1           = ('#32A200', '#F9891B')
POKERED_V_POKEBLUE_S1       = ('#BF586B', '#003DA2')
POKERED_V_POKEGREEN_S1      = ('#BF586B', '#009A6E')
SNOWMEN_V_SANDCASTLES_S1    = ('#0EB6A7', '#FAB01D')
HOVERBOARD_V_JETPACK_S1     = ('#59BE9C', '#E75A2D')
GALLOUT_V_FHEALING_S1       = ('#BC326D', '#C0AE26')
SPONGEBOB_V_PATRICK_S1      = ('#DCA41D', '#E95F9A')
TYNAMAYO_V_REDSALMON_S1     = ('#38C8D0', '#E56F87')
WTOUR_V_SPACEA_S1           = ('#88AF45', '#014BD0')
CALLIE_V_MARIE_S1           = ('#AF16AC', '#71DA0C')
# Other -----------------------------------------------------------------------
DYELLOW_V_DFUCHSIA_S1       = ('#FBD704', '#8C0C7F', '#1BC3D8')
DBLUE_V_ORANGE_S1           = ('#2E0CB5', '#F86300', '#FDFF00')
DFUCHSIA_S1                 = ('#A5267F', '#FFE500')
###############################################################################
# Splatoon 2
###############################################################################
# Regular Battle --------------------------------------------------------------
LEMON_V_PLUM_S2             = ('#BBC905', '#830B9C')
LPINK_V_BLUE_S2             = ('#D60E6E', '#311AA8')
RASPBERRY_V_NYELLOW_S2      = ('#DE0B64', '#BFD002')
GRAPE_V_TURQUOISE_S2        = ('#5F0FB4', '#08B672')
PINK_V_LBLUE_S2             = ('#CB0856', '#0199B8')
DPURPLE_V_ORANGE_S2         = ('#4A14AA', '#FB5C03')
NPINK_V_NGREEN_S2           = ('#CF0466', '#17A80D')
SKY_V_GOLD_S2               = ('#007EDC', '#E1A307')
# Ranked Battle ---------------------------------------------------------------
SGREEN_V_GRAPE_S2           = ('#25B100', '#571DB1', '#CD2D7E')
WGREEN_V_DMAGENTA_S2        = ('#03B362', '#B1008D', '#A8B700')
TURQUOISE_V_PUMPKIN_S2      = ('#0CAE6E', '#F75900', '#6A1EC1')
MUSTARD_V_PURPLE_S2         = ('#CE8003', '#9208B2', '#1AB46A')
BLUE_V_GREEN_S2             = ('#2922B5', '#5EB604', '#CA21A5')
RPURPLE_V_GAPPLE_S2         = ('#7B0393', '#43BA05', '#DB7821')
YELLOW_V_TBLUE_S2           = ('#D9C100', '#007AC9', '#ED580B')
# Octocanyon ------------------------------------------------------------------
YELLOW_V_FUCHSIA_S2         = ('#D9C100', '#D645C8', '#17A80D')
GREEN_V_FUCHSIA_S2          = ('#17A80D', '#D645C8', '#D9C100')
LBLUE_V_FUCHSIA_S2          = ('#03C1CD', '#D645C8', '#D9C100')
# Splatfest -------------------------------------------------------------------
MAYO_V_KETCHUP_S2           = ('#FFE99B', '#FB321E', '#1BB026')
FLIGHT_V_INVINSIBILITY_S2   = ('#4F55ED', '#6BD52C', '#ED1D9A')
FRIES_V_NUGGETS_S2          = ('#E8540A', '#6A3BE0', '#FFCA0E')
FROLL_V_BROLL_S2            = ('#FF7D9A', '#00A0B0', '#E4E567')
VAMPIRE_V_WEREWOLF_S2       = ('#6735AF', '#FE6829', '#00CA0E')
AGILITY_V_ENDURANCE_S2      = ('#F3B000', '#F5498B', '#13A715')
WBREAKFAST_V_CBREAKFAST_S2  = ('#FF5E17', '#00A39A', '#EDD926')
LEMON_V_NLEMON_S2           = ('#BEE600', '#C52ADB', '#00B278')
SCIFI_V_FANTASY_S2          = ('#1FAFE8', '#8BFF06', '#FD636A')
FILM_V_BOOK_S2              = ('#9030FF', '#14B8A0', '#EEC70E')
WINNERW_V_WOUTERW_S2        = ('#FF7536', '#9090BA', '#DC1C1E')
SWEATER_V_SOCKS_S2          = ('#C4354D', '#0D8B51', '#CACACA')
ACTION_V_COMEDY_S2          = ('#FA8E00', '#1384BA', '#B44AEF')
CHAMPION_V_CHALLENGER_S2    = ('#A18E3B', '#1D07AC', '#F52E71')
GHERKOUT_V_GHERKIN_S2       = ('#B14A8D', '#83C91A', '#0FBA9D')
MONEY_V_LOVE_S2             = ('#FFD624', '#FC6D75', '#5451EC')
FLOWER_V_DUMPLING_S2        = ('#FF8787', '#7EC27A', '#ECE8B1')
CHICKEN_V_EGG_S2            = ('#EFF2EB', '#FABF50', '#ED2635')
LMODEL_V_PMODEL_S2          = ('#059E9C', '#C1CC47', '#E2E2E2')
SALTY_V_SWEET_S2            = ('#B1DBD1', '#E29440', '#D94C79')
BASEBALL_V_SOCCER_S2        = ('#FA5A2A', '#00993A', '#6642D0')
UCREATURE_V_ATECHNOLOGY_S2  = ('#FF6D40', '#38377A', '#F1E61C')
PULP_V_NPULP_S2             = ('#EE8122', '#2FCF46', '#42D0EA')
SQUID_V_OCTOPUS_S2          = ('#50D525', '#E900D2', '#4B22C8')
MMOUNTAIN_V_BSVILLAGE_S2    = ('#FFCE0C', '#058F00', '#E24FE5')
ADVENTURE_V_RELAX_S2        = ('#FFB600', '#00967A', '#4B22C8')
FORK_V_SPOON_S2             = ('#E36D60', '#2FB89A', '#EBCD62')
RETRO_V_MODERN_S2           = ('#6B4221', '#596666', '#0118E3')
TSUBUAN_V_KOSHIAN_S2        = ('#655A99', '#88214D', '#78D04F')
TRICK_V_TREAT_S2            = ('#EC7125', '#8805CC', '#4EE69F')
PCHOCOLATE_V_PGOKUBOSO_S2   = ('#E70F21', '#E6E6E6', '#734024')
SALSA_V_GUAC_S2             = ('#801A00', '#757A2B', '#D4C2B5')
EATIT_V_SAVEIT_S2           = ('#C42138', '#A6AD8C', '#6363D6')
HERO_V_VILLAIN_S2           = ('#ED2403', '#4517D1', '#D1D1D1')
FAM_V_FRIEND_S2             = ('#7D5C26', '#82878F', '#C21405')
BOKE_V_TSUKKOMI_S2          = ('#D64703', '#127A87', '#C2238F')
PANCAKE_V_WAFFLE_S2         = ('#D4B873', '#4545AB', '#E64D73')
KNIGHT_V_WIZARD_S2          = ('#788C87', '#6B0A29', '#A67308')
HARE_V_TORTOISE_S2          = ('#E869BF', '#8ACF47', '#17CFDE')
CE_V_PA_S2                  = ('#086312', '#307087', '#BA0A07')
TTRAVEL_V_TELEPORTATION_S2  = ('#695240', '#14247F', '#CFD1C7')
UNICORN_V_NARWHAL_S2        = ('#6B87BF', '#AB66B8', '#D1ED73')
NPINEAPPLE_V_PINEAPPLE_S2   = ('#4A2126', '#ABB012', '#0A6E17')
KID_V_GROWUP_S2             = ('#308766', '#523B40', '#D1ED73')
CHAOS_V_ORDER_S2            = ('#695C3B', '#7F7F99', '#990F2B')
SMUSHROOM_V_SSTAR_S2        = ('#CC1F1F', '#B3A10D', '#0D40DE')
GYELLOW_V_EBLUE_S2          = ('#DEA801', '#4717A9')
# Salmon Run ------------------------------------------------------------------
ORANGE_V_NGREEN_S2          = ('#FB5C03', '#17A80D')
BLUE_NGREEN_S2              = ('#311AA8', '#17A80D')
PINK_V_NGREEN_S2            = ('#CB0856', '#17A80D')
# Octo Expansion --------------------------------------------------------------
BLUE_V_ORANGE_S2            = ('#2E0CB5', '#F86300')
PINK_V_TURQUOISE_S2         = ('#CB0856', '#08B672', '#D9C100')
PEACH_V_TURQUOISE_S2        = ('#FF8787', '#08B672', '#D9C100')
GRAPE_V_TURQUOISE_S2        = ('#5F0FB4', '#08B672', '#D9C100')
###############################################################################
# Splatoon 3
###############################################################################
# Regular Battle --------------------------------------------------------------
PINK_V_GREEN_S3             = ('#C12D74', '#2CB721', '#3A28C4')
ORANGE_V_PURPLE_S3          = ('#CD510A', '#6E04B6', '#94C921')
ORANGE_V_BLUE_S3            = ('#DE6624', '#343BC4', '#CDCD34')
YELLOW_V_PURPLE_S3          = ('#CEB121', '#9025C6', '#5DAB21')
YELLOW_V_BLUE_S3            = ('#D0BE08', '#3A0CCD', '#B62EA7')
LIMEGREEN_V_PURPLE_S3       = ('#BECD41', '#6325CD', '#31C4A9')
TURQUOISE_V_PINK_S3         = ('#1BBEAB', '#C43A6E', '#4E4EDD')
TURQUOISE_V_RED_S3          = ('#1BBEAB', '#D74B31', '#0D0DDC')
BLUE_V_YELLOW_S3            = ('#1A1AAE', '#E38D24', '#CD43A6')
# Splatfest -------------------------------------------------------------------
ROCK_PAPER_SCISSORS_S3      = ('#413BBA', '#BEB013', '#C03E3E', '#35BA49')
GEAR_GRUB_FUN_S3            = ('#8A19F7', '#BE7118', '#28C05E', '#3F2CD2')
GRASS_FIRE_WATER_S3         = ('#1BA974', '#DA4514', '#002AFF', '#FFFF00')
SPICY_SWEET_SOUR_S3         = ('#AD5438', '#9A6FCC', '#A5B533', '#00A2E8')
DARK_MILK_WHITE_S3          = ('#3D1F7A', '#995935', '#D6BF8F', '#FFFF00')
NESSIE_ALIENS_BIGFOOT_S3    = ('#118F32', '#793199', '#A1482B', '#0935A6')
POWER_WISDOM_COURAGE_S3     = ('#AB2A5C', '#488DB5', '#03A65F', '#ba8500')
VANILLA_STRAWBERRY_MINT_S3  = ('#cca770', '#bc6d75', '#2ac29e', '#adff6b')
MONEY_FAME_LOVE             = ('#c8752d', '#73bd49', '#bb497b', '#5998ff')
SHIVER_FRYE_BIGMAN_S3       = ('#253fc5', '#d3b113', '#d80501', '#6dda25')
ZOMBIE_SKELETON_GHOST       = ('#0ca34b', '#b04f23', '#964996', '#bfed1c')
HANDSHAKE_FISTBUMP_HUG      = ('#b02a57', '#c58650', '#97c22a', '#a7ffd3')
FRIDAY_SATURDAY_SUNDAY      = ('#b49109', '#284ca7', '#ab3e28', '#319941')
REDBEAN_CUSTARD_WCREAM      = ('#ab0072', '#b66400', '#c1ae88', '#ffff00')
# Return of the Mammalians ----------------------------------------------------
ORANGE_V_BLUE_S3            = ('#EE8711', '#0943F0', '#81DE17')
YELLOW_V_INDIGO_S3          = ('#DEC109', '#531BBA', '#C920B7')
GREEN_V_BLUE_S3             = ('#51C71B', '#2120CC', '#C920B7')
SODA_V_MAGENTA_S3           = ('#AEF4F0', '#DD0DD3', '#C6D314')
LBLUE_V_BLUE_S3             = ('#14BBE7', '#285EEA', '#C920B7')
BLUE_V_MAGENTA_S3           = ('#1B18D7', '#DD0DD3', '#C6D314')
# Deep Cut --------------------------------------------------------------------
BLUE_FRYE_S3                = ('#373DBB', '#CECE28', '#C920B7')
LIME_SHIVER_S3              = ('#BAD421', '#1021BE', '#A714D4')
ORANGE_BMAN_S3              = ('#E1772B', '#2DD9B6', '#2E14D4')
# Salmon Run ------------------------------------------------------------------
YELLOW_V_DGREEN_S3          = ('#B4D933', '#098A71', '#D611E0')
SYELLOW_V_DGREEN_S3         = ('#DDA024', '#098264', '#E114C3')
ORANGE_V_DGREEN_S3          = ('#C44B21', '#098264', '#DCE317')
PINK_V_DTEAL_S3             = ('#C64184', '#0D6E74', '#E3D704')
PURPLE_V_DGREEN_S3          = ('#9361EA', '#0A7A5E', '#D3DD1E')
BLUE_V_DGREEN_S3            = ('#435BF3', '#067E63', '#E9DD14')
# Color Lock ------------------------------------------------------------------
YELLOW_V_BLUE_LK_S3         = ('#CABA21', '#502EBA', '#B62AA7')
YELLOW_V_DTEAL_LK_S3        = ('#DDD112', '#047B8B', '#ED12E4')
YELLOW_V_BLUE_LK_S3         = ('#D6CD25', '#531BBA', '#C920B7')
YELLOW_V_LBLU_V_DBLU_LK_S3  = ('#BDBA14', '#4E85C1', '#4828AB', '#B0C444')
# Other -----------------------------------------------------------------------
WYELLOW_V_WBLUE_WP_S3       = ('#DACD12', '#4B25C9', '#B62EA7')
ORANGE_V_DGREEN_SR_S3       = ('#C95431', '#03644B', '#E7E710')
TEAL_PURPLE_ORANGE_S3       = ('#1BA974', '#98039B', '#C75304', '#C70864')
###############################################################################
# Compile all colors
###############################################################################
(all_variables, ALL_COLORS) = (list(locals()), [])
for name in all_variables:
    if name.isupper():
        vals = list(eval(name))
        ALL_COLORS.extend(vals)
ALL_COLORS = list(set(ALL_COLORS))
shuffle(ALL_COLORS)

###############################################################################
# Custom Season Colors
###############################################################################
SEASON_COLORS = (
  ('#D01D79', '#1D07AC'), ('#6BFF00', '#1D07AC'),
  ('#E1772B', '#1D07AC'), ('#A714D4', '#1D07AC'),
  ('#6BFF00', '#D01D79'), ('#AEF4F0', '#D01D79'),
  ('#6B87BF', '#D01D79'), ('#E1772B', '#D01D79'),
  ('#D01D79', '#1D07AC'), ('#6BFF00', '#1D07AC'),
  ('#E1772B', '#1D07AC'), ('#A714D4', '#1D07AC'),
  ('#6BFF00', '#D01D79'), ('#AEF4F0', '#D01D79'),
  ('#6B87BF', '#D01D79'), ('#E1772B', '#D01D79'),
  ('#D01D79', '#1D07AC')
)

###############################################################################
# Auxiliary Functions
###############################################################################
def colorPaletteFromHexList(clist):
    c = mcolors.ColorConverter().to_rgba
    clrs = [c(i) for i in clist]
    rvb = mcolors.LinearSegmentedColormap.from_list("", clrs)
    return rvb
