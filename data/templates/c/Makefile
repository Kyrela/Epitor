##
## EPITECH PROJECT, $CURRENT_YEAR$
## $PROJECT_NAME$
## File description:
## $FILE_NAME$
##

.SILENT:

####################################################################### Settings

NAME	= $PROJECT_NAME$
CFLAGS	= -Wall -Wextra
INCLUDE_DIRS	= include
SRC_DIRS	= src

######################################################### Advanced configuration

INCLUDES	= $(call dwildcard,$(INCLUDE_DIRS))
SRC	=	$(call rwildcard,$(SRC_DIRS),*.c)
CFLAGS	+= $(INCLUDES:%=-I %)
OBJ	= $(SRC:.c=.o)
CC	= gcc

rwildcard	= $(foreach d,$(wildcard $(1:=/*)),\
			$(call rwildcard,$d,$2) $(filter $(subst *,%,$2),$d))
dwildcard	= $(foreach d,$1,$(shell test -d $d && find $d -type d))

######################################################################### Colors

CGREEN		=	"\\e[32m"
CRED		=	"\\e[31m"
CYELLOW		=	"\\e[33m"
CBLUE2		=	"\\e[34m"
CGREY		=	"\\e[37m"
CDEFAULT	=	"\\e[39m"

########################################################################## Rules

all:	$(NAME)
	@echo -e "$(CGREEN)✔ All done$(CDEFAULT)"

$(NAME):	$(OBJ)
	@echo -e "$(CYELLOW)⤋ Linking .o files...$(CDEFAULT)"
	$(CC) $^ -o $@ $(CFLAGS)
	@echo -e "$(CGREEN)✔ Compilation succeeded: $(NAME)$(CDEFAULT)"

%.o: %.c
	@echo -e "$(CYELLOW)↓ Compiling $@...$(CDEFAULT)"
	$(CC) -o $@ -c $< $(CFLAGS)

debug:	CFLAGS += -g3
debug:	$(NAME)
	@echo -e "$(CGREEN)⚙ Debug possible on $(NAME)$(CDEFAULT)"

clean:
	find -name "*.o" -delete
	find -name "*.gc*" -delete
	find -name "*~" -delete
	find -name "#*#" -delete
	find -name "*vgcore*" -delete
	find -name "*.out" -delete
	find -name "__pycache__" -delete
	find -name "*.hi" -delete
	@echo -e "$(CGREY)✗ Undesirable files deleted$(CDEFAULT)"

fclean:		clean
	rm -f $(NAME)
	@echo -e "$(CGREY)✗ Binary files deleted$(CDEFAULT)"

re:	fclean $(NAME)
	@echo -e "$(CGREEN)⟳ Re-compilation done$(CDEFAULT)"

########################################################################## Phony

.PHONY: all $(NAME) debug clean fclean re
