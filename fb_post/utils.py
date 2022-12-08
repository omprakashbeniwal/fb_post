from collections import defaultdict
from datetime import datetime

from django.db import transaction
from django.db.models import Count, Case, When, IntegerField, F

from fb_post.models import *
from fb_post.exceptions import InvalidUserException, InvalidPostContent, \
    InvalidPostException, InvalidCommentException, \
    UserCannotDeletePostException


def validate_post(post_id):
    if post_id not in Post.objects.values_list('id', flat=True):
        raise InvalidPostException('InvalidPostException')


def validate_user(user_id):
    if user_id not in User.objects.values_list('id', flat=True):
        raise InvalidUserException('InvalidUserException')


def validate_comment(comment_id):
    if comment_id not in Comment.objects.values_list('id', flat=True):
        raise InvalidCommentException('InvalidCommentException')


def validate_post_content(post_content):
    if len(post_content) == 0:
        raise InvalidPostContent('InvalidPostContent')


def validate_comment_content(comment_content):
    if len(comment_content) == 0:
        raise InvalidCommentException('comment content is empty')


@transaction.atomic
def create_post(user_id, post_content):
    """
    :param user_id:
    :param post_content:
    :return:
    """
    validate_user(user_id)
    validate_post_content(post_content)
    post = Post.objects.create(
        content=post_content, posted_at=datetime.now(), posted_by_id=user_id)
    return post.id


@transaction.atomic
def create_comment(user_id, post_id, comment_content):
    """
    :param user_id:
    :param post_id:
    :param comment_content:
    :return:
    """
    validate_user(user_id)
    validate_post(post_id)
    validate_comment_content(comment_content)
    comment = Comment.objects.create(content=comment_content,
                                     commented_at=datetime.now(),
                                     commented_by_id=user_id, post_id=post_id)
    return comment.id


@transaction.atomic
def reply_to_comment(user_id, comment_id, reply_content):
    """
    :param user_id:
    :param comment_id:
    :param reply_content:
    :return:
    """
    validate_user(user_id)
    validate_comment(comment_id)
    validate_comment_content(reply_content)

    comment = Comment.objects.create(content=reply_content,
                                     commented_at=datetime.now(),
                                     commented_by_id=user_id,
                                     parent_comment_id=comment_id)
    return comment.id


@transaction.atomic
def react_to_post(user_id, post_id, reaction_type):
    """
    :param user_id:
    :param post_id:
    :param reaction_type:
    :return:
    """
    validate_user(user_id)
    validate_post(post_id)

    if user_id not in React.objects.values_list('reacted_by', flat=True):
        React.objects.create(post_id=post_id,
                             reaction=reaction_type,
                             reacted_at=datetime.now(),
                             reacted_by_id=user_id)
    else:
        if reaction_type in React.objects.filter(
                reacted_by_id=user_id, post=post_id).values_list('reaction',
                                                                 flat=True):
            React.objects.filter(
                reacted_by_id=user_id, post=post_id).delete()
        else:
            reaction_id = list(React.objects.filter(reacted_by_id=user_id,
                                                    post=post_id).values_list(
                'id', flat=True))
            React.objects.filter(id=reaction_id[0]).update(
                reaction=reaction_type,
                reacted_at=datetime.now())


@transaction.atomic
def react_to_comment(user_id, comment_id, reaction_type):
    """
    :param user_id:
    :param comment_id:
    :param reaction_type:
    :return:
    """
    validate_user(user_id)
    validate_comment(comment_id)

    User.objects.values_list('id', flat=True)
    if user_id not in React.objects.values_list('reacted_by', flat=True):
        React.objects.create(comment_id=comment_id,
                             reaction=reaction_type,
                             reacted_at=datetime.now(),
                             reacted_by_id=user_id)
    else:
        if reaction_type in React.objects.filter(
                reacted_by_id=user_id, comment_id=comment_id) \
                .values_list('reaction', flat=True):
            React.objects.filter(
                reacted_by_id=user_id, comment_id=comment_id).delete()
        else:
            reaction_id = list(React.objects.filter(reacted_by_id=user_id,
                                                    comment_id=comment_id).values_list(
                'id', flat=True))
            React.objects.filter(id=reaction_id[0]).update(
                reaction=reaction_type,
                reacted_at=datetime.now())


def get_total_reaction_count():
    reaction_count = React.objects.aggregate(count=Count(
        'reaction'))
    return reaction_count


def get_reaction_metrics(post_id):
    """
    :param post_id:
    :return:
    """
    validate_post(post_id)
    reactions = React.objects.filter(
        post=post_id).values('post_id',
                             'reaction').annotate(Count('reaction'))
    reaction_materics = {reaction['reaction']: reaction['reaction__count']
                         for reaction in reactions}
    return reaction_materics


def delete_post(user_id, post_id):
    """
    :param user_id:
    :param post_id:
    :return:
    """
    validate_user(user_id)
    validate_post(post_id)

    if user_id not in Post.objects.filter(id=post_id).values_list(
            'posted_by', flat=True):
        raise UserCannotDeletePostException(
            'User is not the creator of the post')
    else:
        Post.objects.filter(id=post_id).delete()


def get_posts_with_more_positive_reactions():
    positive_reaction = ('TU', 'LI', 'LO', 'HA', 'WO')
    negative_reaction = ('SA', 'AN', 'TD')
    posts = React.objects.values('post_id').annotate(
        positive_reaction_count=Count(Case(
            When(reaction__in=positive_reaction, then=1),
            output_field=IntegerField(),
        )), negative_reaction_count=Count(Case(
            When(reaction__in=negative_reaction, then=1),
            output_field=IntegerField(),
        ))).filter(positive_reaction_count__gt=F('negative_reaction_count')) \
        .values_list('post_id', flat=True)
    return list(posts)


def get_posts_reacted_by_user(user_id):
    """
    :param user_id:
    :return:
    """
    validate_user(user_id)

    posts = Post.objects.filter(react__reacted_by=user_id).values_list('id',
                                                                       flat=True)
    return list(posts)


def get_reactions_to_post(post_id):
    """
    :param post_id:
    :return:
    """
    validate_post(post_id)
    reactions_list = list(React.objects.filter(
        post=post_id).select_related('reacted_by'))
    reactions = [
        {
            "user_id": reaction.reacted_by.id,
            "name": reaction.reacted_by.name,
            "profile_pic": reaction.reacted_by.profile_pic,
            "reaction": reaction.reaction,
        }
        for reaction in reactions_list
    ]
    return reactions


def get_reactions_detail(post_ids):
    """
    :param post_ids:
    :return:
    """
    reactions_list = list(React.objects.filter(
        post_id__in=post_ids).select_related('post'))
    post_id_wise_reaction = defaultdict(list)
    for reaction in reactions_list:
        post_id_wise_reaction[reaction.post_id].append(reaction)

    post_id_wise_reaction_details = defaultdict(list)
    for reactions in reactions_list:
        reaction_detail_dict = dict()
        reaction_detail_dict["count"] = len(post_id_wise_reaction[reactions.post_id])
        type_of_reaction = set()
        for i in post_id_wise_reaction[reactions.post_id]:
            type_of_reaction.add(i.reaction)
        reaction_detail_dict["type"] = set(type_of_reaction)
        post_id_wise_reaction_details[reactions.post_id].append(reaction_detail_dict)
    return post_id_wise_reaction_details


def get_reactions_detail_of_comments(comment_ids):
    """
    :param comment_ids:
    :return:
    """
    reactions_list = list(React.objects.filter(
        comment_id__in=comment_ids).select_related('comment'))
    comment_id_wise_reactions = defaultdict(list)
    for reaction in reactions_list:
        comment_id_wise_reactions[reaction.comment_id].append(reaction)

    comment_id_wise_reactions_details = defaultdict(list)
    for reactions in reactions_list:
        reaction_detail_dict = dict()
        reaction_detail_dict["count"] = len(comment_id_wise_reactions[reactions.comment_id])
        type_of_reaction = set()
        for i in comment_id_wise_reactions[reactions.comment_id]:
            type_of_reaction.add(i.reaction)
        reaction_detail_dict["type"] = list(type_of_reaction)
        comment_id_wise_reactions_details[reactions.comment_id].append(reaction_detail_dict)
    return comment_id_wise_reactions_details


def get_reactions_detail_of_comments_replies(comment_ids):
    """
    :param comment_ids:
    :return:
    """
    reactions_list = list(React.objects.filter(
        comment__parent_comment_id__in=comment_ids).select_related('comment'))
    comment_id_wise_reactions = defaultdict(list)
    for reaction in reactions_list:
        comment_id_wise_reactions[reaction.comment_id].append(reaction)

    comment_id_wise_reactions_details = defaultdict(list)
    for reactions in reactions_list:
        reaction_detail_dict = dict()
        reaction_detail_dict["count"] = len(comment_id_wise_reactions[reactions.comment_id])
        type_of_reaction = set()
        for i in comment_id_wise_reactions[reactions.comment_id]:
            type_of_reaction.add(i.reaction)
        reaction_detail_dict["type"] = list(type_of_reaction)
        comment_id_wise_reactions_details[reactions.comment_id].append(reaction_detail_dict)
    return comment_id_wise_reactions_details


def get_replieses_details(comment_ids):
    """
    :param comment_ids:
    :return:
    """
    reply_list = list(Comment.objects.filter(
        parent_comment_id__in=comment_ids).select_related('commented_by'))
    replies_reactions = get_reactions_detail_of_comments_replies(comment_ids)
    parent_comment_id_wise_reply_details = defaultdict(list)
    for reply in reply_list:
        reactions_details = replies_reactions[reply.id]
        reply_detail = dict()
        reply_detail["comment_id"] = reply.pk
        user_detail_dict = {"user_id": reply.commented_by.id,
                            "name": reply.commented_by.name,
                            "profile_pic": reply.commented_by.profile_pic}
        reply_detail["commenter"] = user_detail_dict
        reply_detail["commented_at"] = str(reply.commented_at)
        reply_detail["comment_content"] = reply.content
        reply_detail["reactions"] = reactions_details
        parent_comment_id_wise_reply_details[reply.parent_comment_id].append(reply_detail)
    return parent_comment_id_wise_reply_details


def get_comments_details(post_ids):
    """
    :param post_ids:
    :return:{1:[{1:}, {]}
    """
    comment_list = list(
        Comment.objects.filter(post_id__in=post_ids).select_related(
            'commented_by'))
    post_id_wise_comments_details_list = defaultdict(list)
    comment_ids = list(Comment.objects.filter(
        post_id__in=post_ids).values_list('id', flat=True)
                       )
    comments_replies = get_replieses_details(comment_ids)
    comments_reactions = get_reactions_detail_of_comments(comment_ids)
    for comment in comment_list:
        replies = comments_replies[comment.id]
        reactions_details = comments_reactions[comment.id]
        comment_details = dict()
        comment_details["comment_id"] = comment.pk
        user_detail_dict = {"user_id": comment.commented_by.id,
                            "name": comment.commented_by.name,
                            "profile_pic": comment.commented_by.profile_pic}
        comment_details["commenter"] = user_detail_dict
        comment_details["commented_at"] = str(comment.commented_at)
        comment_details["comment_content"] = comment.content
        comment_details["reaction"] = reactions_details
        comment_details["replies_count"] = len(replies)
        comment_details["replies"] = replies
        post_id_wise_comments_details_list[comment.post_id].append(comment_details)
    return post_id_wise_comments_details_list


def get_posts(post_ids):
    """
    :param post_ids:
    :return:
    """
    for post_id in post_ids:
        validate_post(post_id)

    post_objs = Post.objects.filter(id__in=post_ids).select_related('posted_by')
    list_of_posts = []
    post_id_wise_comments_details_list = get_comments_details(post_ids)
    post_id_wise_reactions_details = get_reactions_detail(post_ids)
    for post_obj in post_objs:
        comments = post_id_wise_comments_details_list[post_obj.id]
        reactions = post_id_wise_reactions_details[post_obj.id]
        user_detail_dict = {"user_id": post_obj.posted_by.id,
                            "name": post_obj.posted_by.name,
                            "profile_pic": post_obj.posted_by.profile_pic}
        detail_dict = {

            "post_id": post_obj.id,
            "posted_by": user_detail_dict,
            "posted_at": str(post_obj.posted_at),
            "post_content": post_obj.content,
            "reactions": reactions,
            "comments": comments,
            "comments_count": len(comments)
        }
        list_of_posts.append(detail_dict)
    return list_of_posts


def get_user_posts(user_id):
    """
    :param user_id:
    :return:
    """
    validate_user(user_id)

    posts = Post.objects.filter(posted_by_id=user_id).values()
    list_of_post_ids = [post['id'] for post in posts]
    post_list = get_posts(list_of_post_ids)
    return post_list


def get_replies_for_comments(comment_id):
    """
    :param comment_id:
    :return:
    """
    validate_comment(comment_id)

    reply_list = list(Comment.objects.filter(
        parent_comment=comment_id).select_related('commented_by'))
    all_replies = list()
    for reply in reply_list:
        single_reply_detail = dict()
        single_reply_detail["comment_id"] = reply.pk
        user_detail_dict = {"user_id": reply.commented_by.id,
                            "name": reply.commented_by.name,
                            "profile_pic": reply.commented_by.profile_pic}
        single_reply_detail["commenter"] = user_detail_dict
        single_reply_detail["commented_at"] = str(reply.commented_at)
        single_reply_detail["comment_content"] = reply.content
        all_replies.append(single_reply_detail)
    return all_replies
