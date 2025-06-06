from django import template
from boards.models import BoardMember

register = template.Library()

@register.simple_tag(takes_context=True)
def has_board_permission(context, board, required_permission):
    user = context['request'].user
    return BoardMember.user_has_access(board, user, required_permission)

@register.simple_tag(takes_context=True)
def board_permission_label(context, board):
    user = context['request'].user
    permission = BoardMember.get_user_permission(board, user)
    labels = {
        'owner': 'Proprietário',
        'moderator': 'Moderador',
        'editor': 'Editor',
        'viewer': 'Leitor',
        None: 'Sem acesso',
    }
    return labels.get(permission, 'Sem acesso')

