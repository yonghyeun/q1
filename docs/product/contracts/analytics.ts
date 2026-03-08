import type {
  AppVersion,
  SessionId,
  UnixMillis,
  UserId,
  UrlString,
  YouTubeVideoId,
} from "./primitives";
import type {
  FeedFilter,
  OpenMethod,
  NoteId,
  SourceId,
  SourceType,
  TimestampInsertMethod,
} from "./domain";

/**
 * Analytics 이벤트 계약(contracts, SoT).
 *
 * `context/analytics/events.md`에 정의된 MVP 이벤트를 기준으로 한 "정식" 스키마다.
 * WBS/병렬 개발 시 충돌을 줄이기 위해 이벤트 이름/props 키는 안정적으로 유지한다.
 */
export interface AnalyticsCommonProps {
  /** 익명/로컬 유저 식별자(LocalStorage 기반). */
  user_id?: UserId;
  /** 세션 식별자(정의는 바뀔 수 있으나 키는 고정). */
  session_id?: SessionId;
  /** 클라이언트 타임스탬프(Unix ms). */
  client_ts?: UnixMillis;
  /** 이벤트 발생 시점의 앱 버전. */
  app_version?: AppVersion;
}

/** `source_added` 이벤트 props. */
export interface SourceAddedProps {
  source_type: SourceType;
  source_id?: SourceId;
  source_url: UrlString;
}

/** `video_opened` 이벤트 props. */
export interface VideoOpenedProps {
  video_id: YouTubeVideoId;
  open_method: OpenMethod;
  source_id?: SourceId;
  /** feed surface에서 열린 경우에만 채운다. */
  feed_filter?: FeedFilter;
  filter_source_id?: SourceId;
}

/** `video_feed_load_older_clicked` 이벤트 props. */
export interface VideoFeedLoadOlderClickedProps {
  feed_filter: FeedFilter;
  filter_source_id?: SourceId;
  /** MVP 기본값은 보통 `30`. */
  page_size: number;
}

/** `note_created` 이벤트 props. */
export interface NoteCreatedProps {
  note_id: NoteId;
  video_id: YouTubeVideoId;
}

/** `timestamp_inserted` 이벤트 props. */
export interface TimestampInsertedProps {
  note_id: NoteId;
  video_id: YouTubeVideoId;
  /** 영상 시작 기준 정수 초. */
  timestamp_seconds: number;
  method: TimestampInsertMethod;
}

/** `timestamp_clicked` 이벤트 props. */
export interface TimestampClickedProps {
  note_id: NoteId;
  video_id: YouTubeVideoId;
  /** 영상 시작 기준 정수 초. */
  timestamp_seconds: number;
}

export const SEARCH_SCOPES = ["notes", "videos"] as const;
/** 지원하는 검색 범위 유니온. */
export type SearchScope = (typeof SEARCH_SCOPES)[number];

/** `search_used` 이벤트 props (MVP에서는 선택). */
export interface SearchUsedProps {
  scope: SearchScope;
  query_len: number;
}

/** 강타입 tracking helper를 위한 `event_name -> props` 매핑. */
export interface AnalyticsEventPropsMap {
  source_added: SourceAddedProps;
  video_opened: VideoOpenedProps;
  video_feed_load_older_clicked: VideoFeedLoadOlderClickedProps;
  note_created: NoteCreatedProps;
  timestamp_inserted: TimestampInsertedProps;
  timestamp_clicked: TimestampClickedProps;
  search_used: SearchUsedProps;
}

/** 지원하는 전체 이벤트 이름 유니온. */
export type AnalyticsEventName = keyof AnalyticsEventPropsMap;

/**
 * 공통 이벤트 레코드 형태.
 *
 * 구현 메모: 런타임 validation은 아직 포함하지 않는다(추후 점진 도입).
 */
export interface AnalyticsEventRecord<TName extends AnalyticsEventName = AnalyticsEventName> {
  event_name: TName;
  props: AnalyticsEventPropsMap[TName];
  common?: AnalyticsCommonProps;
}

/** MVP 이벤트 레코드 전체(discriminated union). */
export type AnalyticsEvent =
  | AnalyticsEventRecord<"source_added">
  | AnalyticsEventRecord<"video_opened">
  | AnalyticsEventRecord<"video_feed_load_older_clicked">
  | AnalyticsEventRecord<"note_created">
  | AnalyticsEventRecord<"timestamp_inserted">
  | AnalyticsEventRecord<"timestamp_clicked">
  | AnalyticsEventRecord<"search_used">;
