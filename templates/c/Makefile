##
## EPITECH PROJECT, $CURRENT_YEAR$
## $PROJECT_NAME$
## File description:
## $FILE_NAME$
##

SRC	=	src/main.c    \

OBJ	=	$(SRC:.c=.o)

NAME	= $PROJECT_NAME$

CC	=	gcc

CFLAGS	=	-g3

all:	$(NAME)

$(NAME):	$(OBJ)
	$(CC) $(CFLAGS) $(OBJ) -o $(NAME)

clean:
	find -name "*.o" -delete
	find -name "*.gc*" -delete
	find -name "*~" -delete
	find -name "#*#" -delete
	find -name "*vgcore*" -delete
	find -name "*.out" -delete
	find -name "__pycache__" -delete
	find -name "*.hi" -delete

fclean:		clean
	rm -f $(NAME)

re:	fclean all
