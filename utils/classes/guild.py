class Guild:
  __slots__ = ("ID", 
               "name", 
               "welcome_channel", 
               "goodbye_channel", 
               "setup_channel", 
               "ban_words_list"
              )
  def __init__(self, ID, name, welcome_channel, goodbye_channel, setup_channel, ban_words_list):
    self.ID = ID
    self.name = name
    self.welcome_channel = welcome_channel
    self.goodbye_channel = goodbye_channel
    self.setup_channel = setup_channel
    self.ban_words_list = ban_words_list

  def dict_to_guild(d):
    return Guild(
      d['ID'],
      d['name'],
      d['welcome_channel'],
      d['goodbye_channel'],
      d['setup_channel'],
      d['ban_words_list']
    )