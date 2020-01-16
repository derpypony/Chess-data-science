library(readr)
library(dplyr)
library(ggplot2)
library(tidyr)
library(forcats)
library(stringr)

Player_piece_info <- read_csv("Player_piece_info.csv")
# subquestion of question 1
Player_piece_info %>% 
  filter(move_num <= 150) %>% 
  group_by(move_num) %>% 
  summarise(rook = mean(rook),
            queen = mean(queen),
            knight = mean(knight),
            bishop = mean(bishop),
            pawn = mean(pawn),
            count = n()) %>% 
  gather(rook, queen, bishop, knight, pawn, key = 'piece', value = "average_num") %>% 
  rename(move = move_num) %>% 
  ggplot(aes(move, average_num, group = piece, color = piece)) + 
  geom_smooth(method = "lm", formula = y ~ poly(x, 10), se = FALSE) + 
  labs(y = 'average number of pieces on board', title = 'Average Piece count on Board')
# subquestion of question 1

life_span <- function(piece_count, piece){
  if(piece %in% c('rook', 'bishop', 'knight'))
  {
    return(average_life(piece_count, 2))
  }
  else if(piece == 'queen')
  {
    return(average_life(piece_count, 1))
  }
  else
  {
    return(average_life(piece_count, 8))
  }
}

average_life <- function(piece_count, n)
{
  sum = 0
  for (i in 1:n)
  {
    sum = sum + sum(piece_count >= i & piece_count <= n)
  }
  return(sum/n)
}

life_data <- Player_piece_info %>% 
  group_by(file_name, player) %>% 
  summarise(queen = life_span(queen, 'queen'),
            rook = life_span(rook,'rook'),
            bishop = life_span(bishop, 'bishop'),
            knight = life_span(knight, 'knight'),
            pawn = life_span(pawn, 'pawn')) %>% 
  gather(queen, rook, bishop, knight, pawn, key = 'piece', value = 'mean_life_span') %>% 
  ungroup()

life_data <- life_data %>% 
  group_by(player, piece) %>% 
  summarise(mean_life_span = mean(mean_life_span)) %>% 
  ungroup()
# we reuse the following code snap on bishop, knight, queen and rook
life_data %>% 
  filter(piece == 'pawn') %>% 
  mutate(player = fct_reorder(player, mean_life_span)) %>% 
  ggplot() + geom_bar(aes(player, mean_life_span), stat = 'identity') +
  coord_flip() +
  labs(title = 'Average life span of Pawn', x = '', y = 'mean life span')

# subquestion of question 1
game_data <- read_csv("game_data.csv")


count_promote <- function(lines, color){
  if (color == 'White'){
    return (str_count(lines, '8=Q'))
  }
  else{
    return(str_count(lines, '1=Q'))
  }
}

game_data %>% 
  filter(!is.na(lines)) %>% 
  mutate(promote_count = mapply(count_promote, lines, color)) %>% 
  group_by(player) %>% 
  summarise(game_num = n(), promote_total = sum(promote_count)) %>% 
  mutate(average = promote_total / game_num) %>% 
  mutate(player = fct_reorder(player, average)) %>%
  ggplot(aes(player, average)) + 
  geom_bar(stat = "identity") + 
  coord_flip() +
  labs(title = 'Average Number of Pawns Get Promoted to a Queen', x = '', y = 'average number per game')


# second question
# player age, from old to young: Morphy, Capablanca, Alekhine, Botvinnik, Tal, Fischer, Kasparov, Anand, Polgar, nakamura, Carlsen, Caruana
Player_attacked_square_info <- read_csv("Player_attacked_square_info.csv")
Player_attacked_square_info %>% 
  filter(move_num <= 50) %>% 
  group_by(player, move_num) %>% 
  summarise(mean_attacked_square = mean(attacked_square_num)) %>% 
  ungroup() %>% 
  mutate(player = factor(player, ordered = TRUE ,levels = c('Morphy', 'Capablanca', 'Alekhine', 'Botvinnik', 'Tal', 'Fischer', 'Kasparov', 'Anand', 'Polgar', 'Nakamura', 'Carlsen', 'Caruana'))) %>% 
  ggplot(aes(move_num, mean_attacked_square, group = player, color = player)) +
  scale_fill_gradient() +
  geom_smooth(method = "lm", formula = y ~ poly(x, 10), se = FALSE) +
  labs(title = 'Average Attacked Enemy Square Count', x = 'move', y = 'square count')


#Third question
Player_piece_sac_data <- read_csv("Chess/R file/Player_piece_sac_data.csv")
Player_piece_sac_data %>% 
  group_by(player) %>% 
  summarise(total_moves = sum(moves), total_sac = sum(total_sac)) %>% 
  mutate(freq = total_sac / total_moves) %>% 
  mutate(player = fct_reorder(player, freq)) %>% 
  ggplot(aes(player, freq)) + 
  geom_bar(stat = "identity") +
  coord_flip() +
  labs(x = '', y = 'average sac value per move', title = 'Piece Sacrifice for Players')
