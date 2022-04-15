##
## EPITECH PROJECT, $CURRENT_YEAR$
## $PROJECT_NAME$
## File description:
## $FILE_NAME$
##

.SILENT:

NAME	= $PROJECT_NAME$

SRC	=	$(wildcard src/*.c)	\

INCLUDES	= include


OBJ	=	$(SRC:.c=.o)
CC	=	gcc
CFLAGS	=	-Wall -Wextra -g3 $(INCLUDES:%=-I %)

ifndef PERCENT
	T := $(shell $(MAKE) $(MAKECMDGOALS) --no-print-directory \
		-nrRf $(firstword $(MAKEFILE_LIST)) \
	    PERCENT="COUNTTHIS" | grep -c "COUNTTHIS")
    N := x
    C = $(words $N)$(eval N := x $N)
    PERCENT = [`expr $C '*' 100 / $T`%]
endif

all:	$(NAME)
	echo -e "\e[32m$(PERCENT) All done\e[39m"

$(NAME):	$(OBJ)
	echo -e "\e[33m$(PERCENT)\e[37m Linking .o files..."
	$(CC) $(CFLAGS) $^ -o $@
	echo -e "\e[32m$(PERCENT) Compilation succeeded: $(NAME)"

%.o: %.c
	$(CC) $(CFLAGS) -o $@ -c $<
	echo -e "\e[33m$(PERCENT)\e[37m Compiling $@..."

clean:
	find -name "*.o" -delete
	find -name "*.gc*" -delete
	find -name "*~" -delete
	find -name "#*#" -delete
	find -name "*vgcore*" -delete
	find -name "*.out" -delete
	find -name "__pycache__" -delete
	find -name "*.hi" -delete
	echo -e "\e[37m$(PERCENT) Undesirable files deleted"

fclean:		clean
	rm -f $(NAME)
	echo -e "\e[37m$(PERCENT) Binary files deleted"

re:	fclean $(NAME)
	echo -e "\e[32m$(PERCENT) Re-compilation done"

.PHONY: all $(NAME) clean fclean re
