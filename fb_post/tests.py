import json

import pytest

from fb_post.utils import *
from freezegun import freeze_time


@pytest.mark.django_db
def test_create_post_to_validate_user():
    # Arrange
    User.objects.create(name='Rohit',
                        profile_pic='https://www.shutterstock.com/image-photo/large-thick-industrial-black-metal-chain-1081708619')

    # Act
    with pytest.raises(Exception) as e:
        create_post(2, 'first post')

    # Assert
    assert str(e.value) == "InvalidUserException"


@pytest.mark.django_db
def test_create_post_to_validate_post_content():
    # Arrange
    User.objects.create(name='Rohit',
                        profile_pic='https://www.shutterstock.com/image-photo/large-thick-industrial-black-metal-chain-1081708619')

    # Act
    with pytest.raises(Exception) as e:
        create_post(1, '')

    # Assert
    assert str(e.value) == "InvalidPostContent"


@pytest.mark.django_db
def test_create_post():
    # Arrange
    user = User.objects.create(name='Rohit',
                               profile_pic='https://www.shutterstock.com/image-photo/large-thick-industrial-black-metal-chain-1081708619')
    post_id = 1
    # Act
    post_create = create_post(user.id, 'first post')
    # Assert
    assert post_create == post_id


@pytest.mark.django_db
def test_create_comment_to_validate_user():
    # Arrange
    User.objects.create(name='Rohit',
                        profile_pic='https://www.shutterstock.com/image-photo/large-thick-industrial-black-metal-chain-1081708619')

    # Act
    with pytest.raises(Exception) as e:
        create_comment(3, 1, 'first comment')

    # Assert
    assert str(e.value) == "InvalidUserException"


@pytest.mark.django_db
def test_create_comment_to_validate_user():
    # Arrange
    User.objects.create(name='Rohit',
                        profile_pic='https://www.shutterstock.com/image-photo/large-thick-industrial-black-metal-chain-1081708619')

    # Act
    with pytest.raises(Exception) as e:
        create_comment(3, 1, 'first comment')

    # Assert
    assert str(e.value) == "InvalidUserException"


@pytest.mark.django_db
def test_create_comment_to_validate_post():
    # Arrange
    user = User.objects.create(name='Rohit',
                               profile_pic='https://www.shutterstock.com/image-photo/large-thick-industrial-black-metal-chain-1081708619')

    # Act
    with pytest.raises(Exception) as e:
        create_comment(user.id, 1, 'first comment')

    # Assert
    assert str(e.value) == "InvalidPostException"


@pytest.mark.django_db
def test_create_comment_to_validate_comment_content():
    # Arrange
    user = User.objects.create(name='Rohit',
                               profile_pic='https://www.shutterstock.com/image-photo/large-thick-industrial-black-metal-chain-1081708619')
    post = Post.objects.create(content='first post', posted_at=datetime.now(),
                               posted_by_id=user.id)
    # Act
    with pytest.raises(Exception) as e:
        create_comment(user.id, post.id, '')

    # Assert
    assert str(e.value) == "comment content is empty"


@pytest.mark.django_db
def test_create_comment():
    # Arrange
    user = User.objects.create(name='Rohit',
                               profile_pic='https://www.shutterstock.com/image-photo/large-thick-industrial-black-metal-chain-1081708619')
    post = Post.objects.create(content='first post', posted_at=datetime.now(),
                               posted_by_id=user.id)
    comment_id = 1
    # Act
    created_comment = create_comment(user.id, post.id, 'first post')
    # Assert
    assert created_comment == comment_id


@pytest.mark.django_db
def test_reply_to_comment_to_validate_user():
    # Arrange
    User.objects.create(name='Rohit',
                        profile_pic='https://www.shutterstock.com/image-photo/large-thick-industrial-black-metal-chain-1081708619')

    # Act
    with pytest.raises(Exception) as e:
        reply_to_comment(3, 1, 'first reply')

    # Assert
    assert str(e.value) == "InvalidUserException"


@pytest.mark.django_db
def test_reply_to_comment_to_validate_comment():
    # Arrange
    User.objects.create(name='Rohit',
                        profile_pic='https://www.shutterstock.com/image-photo/large-thick-industrial-black-metal-chain-1081708619')

    # Act
    with pytest.raises(Exception) as e:
        reply_to_comment(2, 1, 'first reply')

    # Assert
    assert str(e.value) == "InvalidUserException"


@pytest.mark.django_db
def test_reply_to_comment_to_validate_reply_content():
    # Arrange
    user = User.objects.create(name='Rohit',
                               profile_pic='https://www.shutterstock.com/image-photo/large-thick-industrial-black-metal-chain-1081708619')
    post = Post.objects.create(content='first post', posted_at=datetime.now(),
                               posted_by_id=user.id)
    comment = Comment.objects.create(content='first comment',
                                     commented_at=datetime.now(),
                                     commented_by_id=user.id, post_id=post.id)
    reply_id = 2
    # Act
    create_reply = reply_to_comment(user.id, comment.id, 'first reply')
    # Assert
    assert create_reply == reply_id


@pytest.mark.django_db
def test_react_to_post_validate_user():
    # Arrange
    User.objects.create(name='Rohit',
                        profile_pic='https://www.shutterstock.com/image-photo/large-thick-industrial-black-metal-chain-1081708619')

    # Act
    with pytest.raises(Exception) as e:
        react_to_post(3, 1, 'HA')

    # Assert
    assert str(e.value) == "InvalidUserException"


@pytest.mark.django_db
def test_react_to_post_validate_post():
    # Arrange
    user = User.objects.create(name='Rohit',
                               profile_pic='https://www.shutterstock.com/image-photo/large-thick-industrial-black-metal-chain-1081708619')

    # Act
    with pytest.raises(Exception) as e:
        react_to_post(user.id, 1, 'HA')

    # Assert
    assert str(e.value) == "InvalidPostException"


@pytest.mark.django_db
def test_react_to_post_if_user_has_not_reacted_before():
    # Arrange
    user = User.objects.create(name='Rohit',
                               profile_pic='https://www.shutterstock.com/image-photo/large-thick-industrial-black-metal-chain-1081708619')
    post = Post.objects.create(content='first post', posted_at=datetime.now(),
                               posted_by_id=user.id)
    react_id = 1

    # Act
    react_to_post(user.id, post.id, 'HA')
    x = list(React.objects.filter(reacted_by_id=user.id,
                                  post_id=post.id).values_list(
        'id', flat=True))

    reaction_id = x[0]
    # Assert
    assert reaction_id == react_id


@pytest.mark.django_db
def test_react_to_post_if_user_has_reacted_before():
    # Arrange
    user = User.objects.create(name='Rohit',
                               profile_pic='https://www.shutterstock.com/image-photo/large-thick-industrial-black-metal-chain-1081708619')
    post = Post.objects.create(content='first post', posted_at=datetime.now(),
                               posted_by_id=user.id)
    reaction_id = 1
    react_to_post(user.id, post.id, 'HA')
    # Act
    react_to_post(user.id, post.id, 'AN')
    x = list(React.objects.filter(reacted_by_id=user.id,
                                  post_id=post.id).values_list(
        'id', flat=True))

    reaction = x[0]
    # Assert
    assert reaction == reaction_id


@pytest.mark.django_db
def test_react_to_post_if_user_has_reacted_before_with_different_reaction_updates_the_existing_reaction():
    # Arrange
    user = User.objects.create(name='Rohit',
                               profile_pic='https://www.shutterstock.com/image-photo/large-thick-industrial-black-metal-chain-1081708619')
    post = Post.objects.create(content='first post', posted_at=datetime.now(),
                               posted_by_id=user.id)
    reaction = 'AN'
    react_to_post(user.id, post.id, 'HA')
    # Act
    react_to_post(user.id, post.id, 'AN')
    x = list(React.objects.filter(reacted_by_id=user.id,
                                  post_id=post.id).values_list(
        'reaction', flat=True))

    reaction_type = x[0]
    # Assert
    assert reaction_type == reaction


@pytest.mark.django_db
def test_react_to_post_if_user_has_reacted_before_with_same_reaction_delete_the_existing_reaction():
    # Arrange
    user = User.objects.create(name='Rohit',
                               profile_pic='https://www.shutterstock.com/image-photo/large-thick-industrial-black-metal-chain-1081708619')
    post = Post.objects.create(content='first post', posted_at=datetime.now(),
                               posted_by_id=user.id)
    react_to_post(user.id, post.id, 'HA')
    # Act
    react_to_post(user.id, post.id, 'HA')
    is_exists = React.objects.filter(reacted_by_id=user.id,
                                     post_id=post.id).exists()

    # Assert
    assert is_exists is False


@pytest.mark.django_db
def test_react_to_comment_validate_user():
    # Arrange
    User.objects.create(name='Rohit',
                        profile_pic='https://www.shutterstock.com/image-photo/large-thick-industrial-black-metal-chain-1081708619')

    # Act
    with pytest.raises(Exception) as e:
        react_to_comment(3, 1, 'HA')

    # Assert
    assert str(e.value) == "InvalidUserException"


@pytest.mark.django_db
def test_react_to_comment_validate_comment():
    # Arrange
    user = User.objects.create(name='Rohit',
                               profile_pic='https://www.shutterstock.com/image-photo/large-thick-industrial-black-metal-chain-1081708619')

    # Act
    with pytest.raises(Exception) as e:
        react_to_comment(user.id, 1, 'HA')

    # Assert
    assert str(e.value) == "InvalidCommentException"


@pytest.mark.django_db
def test_react_to_comment_if_user_has_not_reacted_before():
    # Arrange
    user = User.objects.create(name='Rohit',
                               profile_pic='https://www.shutterstock.com/image-photo/large-thick-industrial-black-metal-chain-1081708619')
    post = Post.objects.create(content='first post', posted_at=datetime.now(),
                               posted_by_id=user.id)
    comment = Comment.objects.create(content='first comment',
                                     commented_at=datetime.now(),
                                     commented_by_id=user.id, post_id=post.id)
    react_id = 1

    # Act
    react_to_comment(user.id, post.id, 'HA')
    x = list(React.objects.filter(reacted_by_id=user.id,
                                  comment_id=comment.id).values_list(
        'id', flat=True))

    reaction_id = x[0]
    # Assert
    assert reaction_id == react_id


@pytest.mark.django_db
def test_react_to_comment_if_user_has_reacted_before():
    # Arrange
    user = User.objects.create(name='Rohit',
                               profile_pic='https://www.shutterstock.com/image-photo/large-thick-industrial-black-metal-chain-1081708619')
    post = Post.objects.create(content='first post', posted_at=datetime.now(),
                               posted_by_id=user.id)
    comment = Comment.objects.create(content='first comment',
                                     commented_at=datetime.now(),
                                     commented_by_id=user.id, post_id=post.id)
    react_to_comment(user.id, post.id, 'AN')
    react_id = 1

    # Act
    react_to_comment(user.id, post.id, 'HA')
    x = list(React.objects.filter(reacted_by_id=user.id,
                                  comment_id=comment.id).values_list(
        'id', flat=True))

    reaction_id = x[0]
    # Assert
    assert reaction_id == react_id


@pytest.mark.django_db
def test_react_to_comment_if_user_has_reacted_before_with_different_reaction_updates_the_existing_reaction():
    # Arrange
    user = User.objects.create(name='Rohit',
                               profile_pic='https://www.shutterstock.com/image-photo/large-thick-industrial-black-metal-chain-1081708619')
    post = Post.objects.create(content='first post', posted_at=datetime.now(),
                               posted_by_id=user.id)
    comment = Comment.objects.create(content='first comment',
                                     commented_at=datetime.now(),
                                     commented_by_id=user.id, post_id=post.id)
    react_to_comment(user.id, post.id, 'AN')
    reaction_type = 'HA'

    # Act
    react_to_comment(user.id, post.id, 'HA')
    x = list(React.objects.filter(reacted_by_id=user.id,
                                  comment_id=comment.id).values_list(
        'reaction', flat=True))

    reaction_id = x[0]
    # Assert
    assert reaction_id == reaction_type


@pytest.mark.django_db
def test_react_to_comment_if_user_has_reacted_before_with_same_reaction_delete_the_existing_reaction():
    # Arrange
    user = User.objects.create(name='Rohit',
                               profile_pic='https://www.shutterstock.com/image-photo/large-thick-industrial-black-metal-chain-1081708619')
    post = Post.objects.create(content='first post', posted_at=datetime.now(),
                               posted_by_id=user.id)
    comment = Comment.objects.create(content='first comment',
                                     commented_at=datetime.now(),
                                     commented_by_id=user.id, post_id=post.id)
    react_to_comment(user.id, post.id, 'HA')

    # Act
    react_to_comment(user.id, post.id, 'HA')
    is_exists = React.objects.filter(reacted_by_id=user.id,
                                     comment_id=comment.id).exists()

    # Assert
    assert is_exists is False


@pytest.mark.django_db
def test_get_total_reaction_count_returns_count_of_total_reaction():
    # Arrange
    user = User.objects.create(name='Rohit',
                               profile_pic='https://www.shutterstock.com/image-photo/large-thick-industrial-black-metal-chain-1081708619')
    post = Post.objects.create(content='first post', posted_at=datetime.now(),
                               posted_by_id=user.id)
    React.objects.create(post_id=post.id,
                         reaction='HA',
                         reacted_at=datetime.now(),
                         reacted_by_id=user.id)
    total_count = {'count': 1}
    # Act
    total = get_total_reaction_count()

    # Assert
    assert total == total_count


@pytest.mark.django_db
def test_get_reaction_metrics_validate_post_id():
    # Arrange
    User.objects.create(name='Rohit',
                        profile_pic='https://www.shutterstock.com/image-photo/large-thick-industrial-black-metal-chain-1081708619')

    # Act
    with pytest.raises(Exception) as e:
        get_reaction_metrics(1)

    # Assert
    assert str(e.value) == "InvalidPostException"


@pytest.mark.django_db
def test_get_reaction_metrics_returns_metrics_of_reactions():
    # Arrange
    user_one = User.objects.create(name='Rohit',
                                   profile_pic='https://www.shutterstock.com/image-photo/large-thick-industrial-black-metal-chain-1081708619')
    user_two = User.objects.create(name='Summit',
                                   profile_pic='https://www.shutterstock.com/image-photo/large-thick-industrial-black-metal-chain-1081708619')

    post = Post.objects.create(content='first post', posted_at=datetime.now(),
                               posted_by_id=user_one.id)
    React.objects.create(post_id=post.id,
                         reaction='HA',
                         reacted_at=datetime.now(),
                         reacted_by_id=user_one.id)
    React.objects.create(post_id=post.id,
                         reaction='AN',
                         reacted_at=datetime.now(),
                         reacted_by_id=user_two.id)
    metrics = {'HA': 1, 'AN': 1}

    # Act
    output = get_reaction_metrics(post.id)

    # Assert
    assert output == metrics


@pytest.mark.django_db
def test_delete_post_validate_user_id():
    # Arrange
    User.objects.create(name='Rohit',
                        profile_pic='https://www.shutterstock.com/image-photo/large-thick-industrial-black-metal-chain-1081708619')

    # Act
    with pytest.raises(Exception) as e:
        delete_post(2, 2)
    # Assert
    assert str(e.value) == "InvalidUserException"


@pytest.mark.django_db
def test_delete_post_validate_user_id():
    # Arrange
    User.objects.create(name='Rohit',
                        profile_pic='https://www.shutterstock.com/image-photo/large-thick-industrial-black-metal-chain-1081708619')

    # Act
    with pytest.raises(Exception) as e:
        delete_post(1, 2)
    # Assert
    assert str(e.value) == "InvalidPostException"


@pytest.mark.django_db
def test_delete_post_if_user_is_not_the_creator_of_post():
    # Arrange
    user_one = User.objects.create(name='Rohit',
                                   profile_pic='https://www.shutterstock.com/image-photo/large-thick-industrial-black-metal-chain-1081708619')
    user_two = User.objects.create(name='Summit',
                                   profile_pic='https://www.shutterstock.com/image-photo/large-thick-industrial-black-metal-chain-1081708619')

    post = Post.objects.create(content='first post', posted_at=datetime.now(),
                               posted_by_id=user_one.id)

    # Act
    with pytest.raises(Exception) as e:
        delete_post(user_two.id, post.id)

    # Assert
    assert str(e.value) == "User is not the creator of the post"


@pytest.mark.django_db
def test_delete_post_if_user_is_the_creator_of_post():
    # Arrange
    user_one = User.objects.create(name='Rohit',
                                   profile_pic='https://www.shutterstock.com/image-photo/large-thick-industrial-black-metal-chain-1081708619')
    post = Post.objects.create(content='first post', posted_at=datetime.now(),
                               posted_by_id=user_one.id)

    # Act
    delete_post(user_one.id, post.id)
    does_exists = Post.objects.filter(id=post.id).exists()

    # Assert
    assert does_exists is False


@pytest.mark.django_db
def test_get_posts_with_more_positive_reactions_returns_list_of_post_ids():
    # Arrange
    user_one = User.objects.create(name='Rohit',
                                   profile_pic='https://www.shutterstock.com/image-photo/large-thick-industrial-black-metal-chain-1081708619')
    user_two = User.objects.create(name='Summit',
                                   profile_pic='https://www.shutterstock.com/image-photo/large-thick-industrial-black-metal-chain-1081708619')

    post_one = Post.objects.create(content='first post',
                                   posted_at=datetime.now(),
                                   posted_by_id=user_one.id)
    post_two = Post.objects.create(content='second post',
                                   posted_at=datetime.now(),
                                   posted_by_id=user_two.id)
    React.objects.create(post_id=post_one.id,
                         reaction='HA',
                         reacted_at=datetime.now(),
                         reacted_by_id=user_one.id)
    React.objects.create(post_id=post_two.id,
                         reaction='WO',
                         reacted_at=datetime.now(),
                         reacted_by_id=user_two.id)
    list_of_post_ids = [1, 2]

    # Act
    output = get_posts_with_more_positive_reactions()

    # Assert
    assert output == list_of_post_ids


@pytest.mark.django_db
def test_get_posts_reacted_by_user_validate_user_id():
    # Arrange
    User.objects.create(name='Rohit',
                        profile_pic='https://www.shutterstock.com/image-photo/large-thick-industrial-black-metal-chain-1081708619')

    # Act
    with pytest.raises(Exception) as e:
        get_posts_reacted_by_user(2)
    # Assert
    assert str(e.value) == "InvalidUserException"


@pytest.mark.django_db
def test_get_posts_reacted_by_user_returns_list_of_post_ids():
    # Arrange
    user_one = User.objects.create(name='Rohit',
                                   profile_pic='https://www.shutterstock.com/image-photo/large-thick-industrial-black-metal-chain-1081708619')
    post_one = Post.objects.create(content='first post',
                                   posted_at=datetime.now(),
                                   posted_by_id=user_one.id)
    post_two = Post.objects.create(content='second post',
                                   posted_at=datetime.now(),
                                   posted_by_id=user_one.id)
    React.objects.create(post_id=post_one.id,
                         reaction='HA',
                         reacted_at=datetime.now(),
                         reacted_by_id=user_one.id)
    React.objects.create(post_id=post_two.id,
                         reaction='WO',
                         reacted_at=datetime.now(),
                         reacted_by_id=user_one.id)
    list_of_post_ids = [1, 2]

    # Act
    output = get_posts_reacted_by_user(user_one.id)

    # Assert
    assert output == list_of_post_ids


@pytest.mark.django_db
def test_get_reactions_to_post_validate_post_id():
    # Arrange
    User.objects.create(name='Rohit',
                        profile_pic='https://www.shutterstock.com/image-photo/large-thick-industrial-black-metal-chain-1081708619')

    # Act
    with pytest.raises(Exception) as e:
        get_reactions_to_post(1)
    # Assert
    assert str(e.value) == "InvalidPostException"


@pytest.mark.django_db
def test_get_reactions_to_post_returns_list_of_dictionaries():
    # Arrange
    user_one = User.objects.create(name='Rohit',
                                   profile_pic='https://www.shutterstock.com/image-photo/large-thick-industrial-black-metal-chain-1081708619')
    user_two = User.objects.create(name='Summit',
                                   profile_pic='https://www.shutterstock.com/image-photo/large-thick-industrial-black-metal-chain-1081708619')

    post_one = Post.objects.create(content='first post',
                                   posted_at=datetime.now(),
                                   posted_by_id=user_one.id)
    React.objects.create(post_id=post_one.id,
                         reaction='HA',
                         reacted_at=datetime.now(),
                         reacted_by_id=user_one.id)
    React.objects.create(post_id=post_one.id,
                         reaction='WO',
                         reacted_at=datetime.now(),
                         reacted_by_id=user_two.id)
    list_of_dictionaries = [{'user_id': 1,
                             'name': 'Rohit',
                             'profile_pic': 'https://www.shutterstock.com/image-photo/large-thick-industrial-black-metal-chain-1081708619',
                             'reaction': 'HA'},
                            {'user_id': 2,
                             'name': 'Summit',
                             'profile_pic': 'https://www.shutterstock.com/image-photo/large-thick-industrial-black-metal-chain-1081708619',
                             'reaction': 'WO'}]

    # Act
    output = get_reactions_to_post(post_one.id)

    # Assert
    assert output == list_of_dictionaries


@pytest.mark.django_db
def test_get_reactions_detail_returns_list_of_dictionaries():
    # Arrange
    user_one = User.objects.create(name='Rohit',
                                   profile_pic='https://www.shutterstock.com/image-photo/large-thick-industrial-black-metal-chain-1081708619')
    user_two = User.objects.create(name='Summit',
                                   profile_pic='https://www.shutterstock.com/image-photo/large-thick-industrial-black-metal-chain-1081708619')

    post_one = Post.objects.create(content='first post',
                                   posted_at=datetime.now(),
                                   posted_by_id=user_one.id)
    React.objects.create(post_id=post_one.id,
                         reaction='HA',
                         reacted_at=datetime.now(),
                         reacted_by_id=user_one.id)
    React.objects.create(post_id=post_one.id,
                         reaction='WO',
                         reacted_at=datetime.now(),
                         reacted_by_id=user_two.id)
    list_of_dictionaries = defaultdict(list,
                                       {1: [{'count': 2, 'type': {'HA', 'WO'}},
                                            {'count': 2,
                                             'type': {'HA', 'WO'}}]})

    # Act
    output = get_reactions_detail([post_one.id])

    # Assert
    assert output == list_of_dictionaries


@pytest.mark.django_db
def test_get_reactions_detail_of_comments_returns_list_of_dictionaries():
    # Arrange
    user_one = User.objects.create(name='Rohit',
                                   profile_pic='https://www.shutterstock.com/image-photo/large-thick-industrial-black-metal-chain-1081708619')
    post_one = Post.objects.create(content='first post',
                                   posted_at=datetime.now(),
                                   posted_by_id=user_one.id)
    comment_one = Comment.objects.create(content='first comment',
                                         commented_at=datetime.now(),
                                         commented_by=user_one,
                                         post_id=post_one.id)
    React.objects.create(comment_id=comment_one.id,
                         reaction='HA',
                         reacted_at=datetime.now(),
                         reacted_by_id=user_one.id)

    list_of_dictionaries = defaultdict(list,
                                       {1: [{'count': 1, 'type': ['HA']}]})

    # Act
    output = get_reactions_detail_of_comments([post_one.id])

    # Assert
    assert output == list_of_dictionaries


@pytest.mark.django_db
def test_get_reactions_detail_of_comments_replies_returns_list_of_dictionaries():
    # Arrange
    user_one = User.objects.create(name='Rohit',
                                   profile_pic='https://www.shutterstock.com/image-photo/large-thick-industrial-black-metal-chain-1081708619')
    post_one = Post.objects.create(content='first post',
                                   posted_at=datetime.now(),
                                   posted_by_id=user_one.id)
    comment_one = Comment.objects.create(content='first comment',
                                         commented_at=datetime.now(),
                                         commented_by=user_one,
                                         post_id=post_one.id)
    reply_one = Comment.objects.create(content='first comment',
                                       commented_at=datetime.now(),
                                       commented_by=user_one,
                                       parent_comment_id=comment_one.id)
    React.objects.create(comment_id=reply_one.id,
                         reaction='HA',
                         reacted_at=datetime.now(),
                         reacted_by_id=user_one.id)

    list_of_dictionaries = defaultdict(list, {2: [{'count': 1, 'type': [
        'HA']}]})

    # Act
    output = get_reactions_detail_of_comments_replies([comment_one.id])

    # Assert
    assert output == list_of_dictionaries


@freeze_time("2022-11-14 05:52:30+00:00", tz_offset=-4)
@pytest.mark.django_db
def test_get_replieses_details_returns_list_of_dictionaries():
    # Arrange
    user_one = User.objects.create(name='Rohit',
                                   profile_pic='https://www.shutterstock.com/image-photo/large-thick-industrial-black-metal-chain-1081708619')
    post_one = Post.objects.create(content='first post',
                                   posted_at=datetime.now(),
                                   posted_by_id=user_one.id)
    comment_one = Comment.objects.create(content='first comment',
                                         commented_at=datetime.now(),
                                         commented_by=user_one,
                                         post_id=post_one.id)
    reply_one = Comment.objects.create(content='first reply',
                                       commented_at=datetime.now(),
                                       commented_by=user_one,
                                       parent_comment_id=comment_one.id)
    React.objects.create(comment_id=reply_one.id,
                         reaction='HA',
                         reacted_at=datetime.now(),
                         reacted_by_id=user_one.id)

    list_of_dictionaries = defaultdict(list,
                                       {1: [{'comment_id': 2,
                                             'commenter': {'user_id': 1,
                                                           'name': 'Rohit',
                                                           'profile_pic': 'https://www.shutterstock.com/image-photo/large-thick-industrial-black-metal-chain-1081708619'},
                                             'commented_at': '2022-11-14 '
                                                             '01:52:30+00:00',
                                             'comment_content': 'first reply',
                                             'reactions': [{'count': 1,
                                                            'type': ['HA']}]}]})

    # Act
    output = get_replieses_details([comment_one.id])

    # Assert
    assert output == list_of_dictionaries


@freeze_time("2022-11-14 05:52:30+00:00", tz_offset=-4)
@pytest.mark.django_db
def test_get_comments_details_returns_list_of_dictionaries():
    # Arrange
    user_one = User.objects.create(name='Rohit',
                                   profile_pic='https://www.shutterstock.com/image-photo/large-thick-industrial-black-metal-chain-1081708619')
    post_one = Post.objects.create(content='first post',
                                   posted_at=datetime.now(),
                                   posted_by_id=user_one.id)
    comment_one = Comment.objects.create(content='first comment',
                                         commented_at=datetime.now(),
                                         commented_by=user_one,
                                         post_id=post_one.id)
    comment_two = Comment.objects.create(content='second comment',
                                         commented_at=datetime.now(),
                                         commented_by=user_one,
                                         post_id=post_one.id)
    React.objects.create(comment_id=comment_one.id,
                         reaction='HA',
                         reacted_at=datetime.now(),
                         reacted_by_id=user_one.id)
    React.objects.create(comment_id=comment_two.id,
                         reaction='WO',
                         reacted_at=datetime.now(),
                         reacted_by_id=user_one.id)

    list_of_dictionaries = defaultdict(list,
                                       {1: [{'comment_id': 1,
                                             'commenter': {'user_id': 1,
                                                           'name': 'Rohit',
                                                           'profile_pic': 'https://www.shutterstock.com/image-photo/large-thick-industrial-black-metal-chain-1081708619'},
                                             'commented_at': '2022-11-14 ''01:52:30+00:00',
                                             'comment_content': 'first comment',
                                             'reaction': [
                                                 {'count': 1, 'type': ['HA']}],
                                             'replies_count': 0,
                                             'replies': []},
                                            {'comment_id': 2,
                                             'commenter': {'user_id': 1,
                                                           'name': 'Rohit',
                                                           'profile_pic': 'https://www.shutterstock.com/image-photo/large-thick-industrial-black-metal-chain-1081708619'},
                                             'commented_at': '2022-11-14 ''01:52:30+00:00',
                                             'comment_content': 'second comment',
                                             'reaction': [
                                                 {'count': 1, 'type': ['WO']}],
                                             'replies_count': 0,
                                             'replies': []}]})

    # Act
    output = get_comments_details([post_one.id])

    # Assert
    assert output == list_of_dictionaries


@freeze_time("2022-11-14 05:52:30+00:00", tz_offset=-4)
@pytest.mark.django_db
def test_get_posts_returns_list_of_dictionaries():
    # Arrange
    user_one = User.objects.create(name='Rohit',
                                   profile_pic='https://www.shutterstock.com/image-photo/large-thick-industrial-black-metal-chain-1081708619')
    post_one = Post.objects.create(content='first post',
                                   posted_at=datetime.now(),
                                   posted_by_id=user_one.id)
    comment_one = Comment.objects.create(content='first comment',
                                         commented_at=datetime.now(),
                                         commented_by=user_one,
                                         post_id=post_one.id)
    comment_two = Comment.objects.create(content='second comment',
                                         commented_at=datetime.now(),
                                         commented_by=user_one,
                                         post_id=post_one.id)
    React.objects.create(comment_id=comment_one.id,
                         reaction='HA',
                         reacted_at=datetime.now(),
                         reacted_by_id=user_one.id)
    React.objects.create(comment_id=comment_two.id,
                         reaction='WO',
                         reacted_at=datetime.now(),
                         reacted_by_id=user_one.id)

    list_of_dictionaries = [{'post_id': 1,
                             'posted_by': {'user_id': 1,
                                           'name': 'Rohit',
                                           'profile_pic':
                                               'https://www.shutterstock.com/image-photo/large-thick-industrial-black-metal-chain-1081708619'},
                             'posted_at': '2022-11-14 ''01:52:30+00:00',
                             'post_content': 'first post',
                             'reactions': [],
                             'comments': [{'comment_id': 1,
                                           'commenter': {'user_id': 1,
                                                         'name': 'Rohit',
                                                         'profile_pic': 'https://www.shutterstock.com/image-photo/large-thick-industrial-black-metal-chain-1081708619'},
                                           'commented_at': '2022-11-14 ''01:52:30+00:00',
                                           'comment_content': 'first comment',
                                           'reaction': [
                                               {'count': 1, 'type': ['HA']}],
                                           'replies_count': 0,
                                           'replies': []},
                                          {'comment_id': 2,
                                           'commenter': {'user_id': 1,
                                                         'name': 'Rohit',
                                                         'profile_pic': 'https://www.shutterstock.com/image-photo/large-thick-industrial-black-metal-chain-1081708619'},
                                           'commented_at': '2022-11-14 ''01:52:30+00:00',
                                           'comment_content': 'second comment',
                                           'reaction': [
                                               {'count': 1, 'type': ['WO']}],
                                           'replies_count': 0,
                                           'replies': []}],
                             'comments_count': 2}]

    # Act
    output = get_posts([post_one.id])

    # Assert
    assert output == list_of_dictionaries


@freeze_time("2022-11-14 05:52:30+00:00", tz_offset=-4)
@pytest.mark.django_db
def test_get_user_posts_validate_user():
    # Arrange
    user_one = User.objects.create(name='Rohit',
                                   profile_pic='https://www.shutterstock.com/image-photo/large-thick-industrial-black-metal-chain-1081708619')
    post_one = Post.objects.create(content='first post',
                                   posted_at=datetime.now(),
                                   posted_by_id=user_one.id)
    comment_one = Comment.objects.create(content='first comment',
                                         commented_at=datetime.now(),
                                         commented_by=user_one,
                                         post_id=post_one.id)
    comment_two = Comment.objects.create(content='second comment',
                                         commented_at=datetime.now(),
                                         commented_by=user_one,
                                         post_id=post_one.id)
    React.objects.create(comment_id=comment_one.id,
                         reaction='HA',
                         reacted_at=datetime.now(),
                         reacted_by_id=user_one.id)
    React.objects.create(comment_id=comment_two.id,
                         reaction='WO',
                         reacted_at=datetime.now(),
                         reacted_by_id=user_one.id)

    # Act
    with pytest.raises(Exception) as e:
        get_user_posts(2)
    # Assert
    assert str(e.value) == "InvalidUserException"


@freeze_time("2022-11-14 05:52:30+00:00", tz_offset=-4)
@pytest.mark.django_db
def test_get_user_posts_returns_list_of_dictionaries():
    # Arrange
    user_one = User.objects.create(name='Rohit',
                                   profile_pic='https://www.shutterstock.com/image-photo/large-thick-industrial-black-metal-chain-1081708619')
    post_one = Post.objects.create(content='first post',
                                   posted_at=datetime.now(),
                                   posted_by_id=user_one.id)
    comment_one = Comment.objects.create(content='first comment',
                                         commented_at=datetime.now(),
                                         commented_by=user_one,
                                         post_id=post_one.id)
    comment_two = Comment.objects.create(content='second comment',
                                         commented_at=datetime.now(),
                                         commented_by=user_one,
                                         post_id=post_one.id)
    React.objects.create(comment_id=comment_one.id,
                         reaction='HA',
                         reacted_at=datetime.now(),
                         reacted_by_id=user_one.id)
    React.objects.create(comment_id=comment_two.id,
                         reaction='WO',
                         reacted_at=datetime.now(),
                         reacted_by_id=user_one.id)

    list_of_dictionaries = [{'post_id': 1,
                             'posted_by': {'user_id': 1,
                                           'name': 'Rohit',
                                           'profile_pic':
                                               'https://www.shutterstock.com/image-photo/large-thick-industrial-black-metal-chain-1081708619'},
                             'posted_at': '2022-11-14 ''01:52:30+00:00',
                             'post_content': 'first post',
                             'reactions': [],
                             'comments': [{'comment_id': 1,
                                           'commenter': {'user_id': 1,
                                                         'name': 'Rohit',
                                                         'profile_pic': 'https://www.shutterstock.com/image-photo/large-thick-industrial-black-metal-chain-1081708619'},
                                           'commented_at': '2022-11-14 ''01:52:30+00:00',
                                           'comment_content': 'first comment',
                                           'reaction': [
                                               {'count': 1, 'type': ['HA']}],
                                           'replies_count': 0,
                                           'replies': []},
                                          {'comment_id': 2,
                                           'commenter': {'user_id': 1,
                                                         'name': 'Rohit',
                                                         'profile_pic': 'https://www.shutterstock.com/image-photo/large-thick-industrial-black-metal-chain-1081708619'},
                                           'commented_at': '2022-11-14 ''01:52:30+00:00',
                                           'comment_content': 'second comment',
                                           'reaction': [
                                               {'count': 1, 'type': ['WO']}],
                                           'replies_count': 0,
                                           'replies': []}],
                             'comments_count': 2}]

    # Act
    output = get_user_posts(user_one.id)

    # Assert
    assert output == list_of_dictionaries


@freeze_time("2022-11-14 05:52:30+00:00", tz_offset=-4)
@pytest.mark.django_db
def test_get_replies_for_comments_validate_comment():
    # Arrange
    user_one = User.objects.create(name='Rohit',
                                   profile_pic='https://www.shutterstock.com/image-photo/large-thick-industrial-black-metal-chain-1081708619')
    post_one = Post.objects.create(content='first post',
                                   posted_at=datetime.now(),
                                   posted_by_id=user_one.id)
    comment_one = Comment.objects.create(content='first comment',
                                         commented_at=datetime.now(),
                                         commented_by=user_one,
                                         post_id=post_one.id)
    comment_two = Comment.objects.create(content='second comment',
                                         commented_at=datetime.now(),
                                         commented_by=user_one,
                                         post_id=post_one.id)
    React.objects.create(comment_id=comment_one.id,
                         reaction='HA',
                         reacted_at=datetime.now(),
                         reacted_by_id=user_one.id)
    React.objects.create(comment_id=comment_two.id,
                         reaction='WO',
                         reacted_at=datetime.now(),
                         reacted_by_id=user_one.id)

    # Act
    with pytest.raises(Exception) as e:
        get_replies_for_comments(3)
    # Assert
    assert str(e.value) == "InvalidCommentException"


@freeze_time("2022-11-14 05:52:30+00:00", tz_offset=-4)
@pytest.mark.django_db
def test_get_replies_for_comments_returns_list_of_dictionaries(snapshot):
    # Arrange
    user_one = User.objects.create(name='Rohit',
                                   profile_pic='https://www.shutterstock.com/image-photo/large-thick-industrial-black-metal-chain-1081708619')
    post_one = Post.objects.create(content='first post',
                                   posted_at=datetime.now(),
                                   posted_by_id=user_one.id)
    comment_one = Comment.objects.create(content='first comment',
                                         commented_at=datetime.now(),
                                         commented_by=user_one,
                                         post_id=post_one.id)
    Comment.objects.create(content='first reply',
                           commented_at=datetime.now(),
                           commented_by=user_one,
                           parent_comment_id=comment_one.id)

    list_of_dictionaries = [{'comment_id': 2,
                             'commenter': {'user_id': 1,
                                           'name': 'Rohit',
                                           'profile_pic': 'https://www.shutterstock.com/image-photo/large-thick'
                                                          '-industrial-black-metal-chain-1081708619'},
                             'commented_at': '2022-11-14 01:52:30+00:00',
                             'comment_content': 'first reply'}]

    # Act
    response = get_replies_for_comments(comment_one.id)

    # Assert
    k = json.dumps(list_of_dictionaries)
    snapshot.assert_match(k, response)
